import pkg_resources
import os

from .binubuo import binubuo
from .BinubuoTemplate import BinubuoTemplate

# Check if we have configuration somewhere else than home directory
if "BINUBUO_HOME" in os.environ:
    # Look for config file here
    pass
elif 1 == 1:
    # Check for config file in users HOME
    pass
elif 2 == 2:
    # Check for config file in current directory
    pass
else:
    # No config file exists, just set defaults if needed
    pass

# Get packages available for us. We need to check if the pre-requisites for the different database
# options are available when importing them.
pkgs_installed = {pkg.key for pkg in pkg_resources.working_set}

# Oracle requirements
oracle_required = {'cx-oracle'}
oracle_missing = oracle_required - pkgs_installed

if oracle_missing:
    print("Oracle client not installed. Please install cx_Oracle for Oracle support.")
else:
    from .binubuoOracle import binubuoOracle

# Postgres requirements
postgres_required = {'psycopg2'}
postgres_missing = postgres_required - pkgs_installed

if postgres_missing:
    # Check for binary also
    postgres_bin_required = {'psycopg2-binary'}
    postgres_bin_missing = postgres_bin_required - pkgs_installed
    if postgres_bin_missing:
        print("Postgres client not installed. Please install Psycopg2 for Postgres support.")
    else:
        from .binubuoPostgres import binubuoPostgres
else:
    from .binubuoPostgres import binubuoPostgres

# SQL Server requirements
sqlserver_required = {'pyodbc'}
sqlserver_missing = sqlserver_required - pkgs_installed

if oracle_missing:
    print("SQL Server client not installed. Please install pyodbc for SQL Server support.")
else:
    from .binubuoSQLServer import binubuoSQLServer