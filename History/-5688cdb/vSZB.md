# SQL Alchemy

![](./images/sqlalchemy_onion.png)

Working from inside out

## Python DBAPI

- DBAPI, based on Python PEP-024 Database API
- Inconsistent PEP
- six different formats
- Basicly ased on connection and cursor.
  - Connection: Parameters for automation
  - The cursor is the way u execute sql statements.
  - Rollback on the connection.
  - autocommit is done here
- The engine provides a facade over the python DBAPI
  - Transaction control
  - driver specific quirks
- Execution isolation level
  - Use auto commit to be very fast
  - A transaction is the commit, execution and rollback