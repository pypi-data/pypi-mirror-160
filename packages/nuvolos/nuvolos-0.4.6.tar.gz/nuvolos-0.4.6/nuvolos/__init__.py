import getpass
import logging
import os
import re
from configparser import ConfigParser
from urllib.parse import quote

import keyring
import snowflake.connector
from sqlalchemy import create_engine
from .version import __version__
from .sql_utils import to_sql


logger = logging.getLogger(__name__)


def load_env_var(env_var_name, description, print_value=False):
    var = os.getenv(env_var_name)
    if var is None:
        logger.debug(f"Could not find {description} in env var {env_var_name}")
    else:
        if print_value:
            logger.debug(f"Found {description} {var} in env var {env_var_name}")
        else:
            logger.debug(f"Found {description} in env var {env_var_name}")
    return var


def credd_from_env_vars():
    username = load_env_var("NUVOLOS_USERNAME", "username", print_value=True)
    password = load_env_var("NUVOLOS_SF_TOKEN", "Snowflake token", print_value=False)
    if username is None or password is None:
        return None
    else:
        return {"username": username, "snowflake_access_token": password}


def credd_from_odbc_ini():
    credential_filename = os.getenv(
        "NUVOLOS_CREDENTIAL_FILENAME", os.path.expanduser("~") + "/.odbc.ini"
    )
    credential_section = os.getenv("NUVOLOS_CREDENTIAL_SECTION", "nuvolos")
    # Create engine with credentials
    cred = ConfigParser(interpolation=None)
    if not os.path.exists(credential_filename):
        logger.debug(f"Credentials file {credential_filename} not found")
        return None
    cred.read(credential_filename)
    if not cred.has_section(credential_section):
        logger.debug(
            f"Could not find section '{credential_section}' in odbc.ini file {credential_filename}. "
            f"Please add your Nuvolos Snowflake credentials there "
            f"(your username as 'uid' and your Snowflake access token as 'pwd')."
        )
    try:
        odbc_ini = dict(cred.items(credential_section))
    except:
        odbc_ini = {}

    if "uid" not in odbc_ini:
        logger.debug(
            f"Could not find option 'uid' in the '{credential_section}' "
            f"section of odbc.ini file {credential_filename}. "
            f"Please set it to your Nuvolos username"
        )
        return None
    if "pwd" not in odbc_ini:
        logger.debug(
            f"Could not find option 'pwd' in the '{credential_section}' "
            f"section of odbc.ini file {credential_filename}. "
            f"Please set it to your Nuvolos Snowflake access token"
        )
        return None
    logger.debug(f"Found username and snowflake_access_token in {credential_filename}")
    return {"username": odbc_ini["uid"], "snowflake_access_token": odbc_ini["pwd"]}


def credd_from_secrets():
    username_filename = os.getenv("NUVOLOS_USERNAME_FILENAME", "/secrets/username")
    snowflake_access_token_filename = os.getenv(
        "NUVOLOS_SNOWFLAKE_ACCESSS_TOKEN_FILENAME",
        "/secrets/snowflake_access_token",
    )
    if not os.path.exists(username_filename):
        logger.debug(f"Could not find secret file {username_filename}")
        return None
    if not os.path.exists(snowflake_access_token_filename):
        logger.debug(f"Could not find secret file {snowflake_access_token_filename}")
        return None
    with open(username_filename) as username, open(
        snowflake_access_token_filename
    ) as access_token:
        username = username.readline()
        password = access_token.readline()
        logger.debug(f"Found username and Snowflake access token in /secrets files")
        return {"username": username, "snowflake_access_token": password}


def input_nuvolos_credential():
    # store username & password
    username = getpass.getpass("Please input your Nuvolos username:")
    keyring.set_password("nuvolos", "username", username)

    password = getpass.getpass("Please input your Nuvolos password:")
    keyring.set_password("nuvolos", username, password)


def credd_from_local():
    # retrieve username & password
    username = keyring.get_password("nuvolos", "username")
    password = keyring.get_password("nuvolos", username) if username else None
    return {"username": username, "snowflake_access_token": password}


def dbpath_from_file(path_filename):
    if not os.path.exists(path_filename):
        logger.debug(f"Could not find dbpath file {path_filename}")
        return None
    with open(path_filename, "r") as path_file:
        lines = path_file.readlines()
        if len(lines) == 0:
            logger.debug(f"Could not parse dbpath file: {path_filename} is empty.")
            return None
        first_line = lines[0].rstrip()
        if "Tables are not enabled" in first_line:
            raise Exception(
                f"Tables are not enabled for this space, please enable them first"
            )
        # Split at "." character
        # This should have resulted in two substrings
        split_arr = re.split('"."', first_line)
        if len(split_arr) != 2:
            logger.debug(
                f'Could not parse dbpath file: pattern "." not found in {path_filename}. '
                f"Are the names escaped with double quotes?"
            )
            return None
        # Remove the remaining double quotes, as we'll escape those
        db_name = split_arr[0].replace('"', "")
        schema_name = split_arr[1].replace('"', "")
        logger.debug(
            f"Found database = {db_name}, schema = {schema_name} in dbpath file {path_filename}."
        )
        return {"db_name": db_name, "schema_name": schema_name}


def dbpath_from_env_vars():
    db_name = load_env_var("NUVOLOS_DB", "Snowflake database", print_value=True)
    schema_name = load_env_var("NUVOLOS_SCHEMA", "Snowflake schema", print_value=True)
    if db_name is None or schema_name is None:
        return None
    return {"db_name": db_name, "schema_name": schema_name}


def _get_connection_params(username=None, password=None, dbname=None, schemaname=None):
    if username is None and password is None:
        credd = (
            credd_from_secrets()
            or credd_from_env_vars()
            or credd_from_odbc_ini()
            or credd_from_local()
        )
        if (
            credd is None
            or credd.get("username") is None
            or credd.get("snowflake_access_token") is None
        ):
            input_nuvolos_credential()
            credd = credd_from_local()

        username = credd["username"]
        password = credd["snowflake_access_token"]
    elif username is not None and password is None:
        raise ValueError(
            "You have provided a username but not a password. "
            "Please either provide both arguments or leave both arguments empty."
        )
    elif username is None and password is not None:
        raise ValueError(
            "You have provided a password but not a username. "
            "Please either provide both arguments or leave both arguments empty."
        )
    else:
        logger.debug(f"Found username and Snowflake access token as input arguments")

    if dbname is None and schemaname is None:
        path_filename = os.getenv("NUVOLOS_DBPATH_FILE", "/lifecycle/.dbpath")
        dbd = (
            dbpath_from_file(path_filename)
            or dbpath_from_file(".dbpath")
            or dbpath_from_env_vars()
        )
        if dbd is None:
            raise ValueError(
                "Could not find Snowflake database and schema in .dbpath files or env vars. "
                "If you're not using this function from Nuvolos, "
                "please specify the Snowflake database and schema names as input arguments"
            )
        else:
            db_name = dbd["db_name"]
            schema_name = dbd["schema_name"]
    elif dbname is not None and schemaname is None:
        raise ValueError(
            "You have provided a dbname argument but not a schemaname argument. "
            "Please either provide both or provide none of them."
        )
    elif dbname is None and schemaname is not None:
        raise ValueError(
            "You have provided a schemaname argument but not a dbname argument. "
            "Please either provide both or provide none of them."
        )
    else:
        db_name = dbname
        schema_name = schemaname
        logger.debug(f"Found database and schema as input arguments")

    default_snowflake_host = (
        "acstg.eu-central-1" if "STAGING/" in db_name else "alphacruncher.eu-central-1"
    )
    snowflake_host = os.getenv("NUVOLOS_SNOWFLAKE_HOST", default_snowflake_host)
    return username, password, snowflake_host, db_name, schema_name


def get_url(username=None, password=None, dbname=None, schemaname=None):
    """
    Returns an SQLAlchemy connection URL which can be used to create a connection to Nuvolos.
    :param username: Nuvolos user name.
    :param password: Nuvolos password.
    :param dbname: Nuvolos database name from the Connection Guide.
    :param schemaname: Nuvolos schema name from the Connection Guide.
    :return: An SQLAlchemy connection URL representing the Nuvolos connection.
    """
    username, password, snowflake_host, db_name, schema_name = _get_connection_params(
        username=username, password=password, dbname=dbname, schemaname=schemaname
    )
    url = (
        "snowflake://" + quote(username) + ":" + quote(password) + "@" + snowflake_host
    )
    masked_url = (
        "snowflake://" + quote(username) + ":" + "********" + "@" + snowflake_host
    )

    params = (
        "/?database=%22"
        + quote(db_name)
        + "%22"
        + "&schema=%22"
        + quote(schema_name)
        + "%22"
        + "&CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX=TRUE"
        + "&VALIDATEDEFAULTPARAMETERS=TRUE"
    )
    url = url + params
    masked_url = masked_url + params
    logger.debug("Built SQLAlchemy URL: " + masked_url)
    return url


def get_engine(username=None, password=None, dbname=None, schemaname=None):
    """
    Returns an SQLAlchemy Engine object which can be used with Pandas read_sql/to_sql functions.
    :param username: Nuvolos user name.
    :param password: Nuvolos password.
    :param dbname: Nuvolos database name from the Connection Guide.
    :param schemaname: Nuvolos schema name from the Connection Guide.
    :return: A SQLAlchemy Engine object.
    """
    return create_engine(
        url=get_url(username, password, dbname, schemaname),
        echo=False,
        connect_args={
            "QUERY_TAG": f"nuvolos {__version__}",
        },
    )


def get_connection(username=None, password=None, dbname=None, schemaname=None):
    loc_eng = get_engine(username, password, dbname, schemaname)
    return loc_eng.connect()


def get_raw_connection(username=None, password=None, dbname=None, schemaname=None):
    """
    Returns a raw Snowflake Python Connector API Connection object.
    :param username: Nuvolos user name.
    :param password: Nuvolos password.
    :param dbname: Nuvolos database name from the Connection Guide.
    :param schemaname: Nuvolos schema name from the Connection Guide.
    :return: A snowflake.connector.Connection object
    """
    username, password, snowflake_host, db_name, schema_name = _get_connection_params(
        username=username, password=password, dbname=dbname, schemaname=schemaname
    )
    return snowflake.connector.connect(
        user=username,
        password=password,
        account=snowflake_host,
        database=db_name,
        schema=schema_name,
        session_parameters={
            "QUERY_TAG": f"nuvolos {__version__}",
        },
    )
