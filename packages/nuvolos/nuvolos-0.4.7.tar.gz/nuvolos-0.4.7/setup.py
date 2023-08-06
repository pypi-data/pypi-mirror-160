from setuptools import setup, find_packages


def readme():
    with open("README.rst") as f:
        return f.read()


exec(open("nuvolos/version.py").read())
setup(
    name="nuvolos",
    version=__version__,
    description="The Nuvolos python library for database connectivity",
    long_description=readme(),
    url="https://github.com/nuvolos-cloud/python-connector",
    author="Alphacruncher",
    author_email="support@nuvolos.cloud",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "keyring",
        "pyarrow!=8.0.0",
        "sqlalchemy>='1.4.0'",
        "pandas>=1.1.0",
        "snowflake-connector-python>2.6.1",
        "snowflake-sqlalchemy!=1.4.0",
    ],
    zip_safe=False,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
