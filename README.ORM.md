ORM Documentation
=================

This version of XALT uses an object-relational mapper ([SQLAlchemy](http://www.sqlalchemy.org/))
to map Python classes to database objects.
This abstracts the database away from the Python code and gives additional flexibility.

Installation Requirements
-------------------------

* SQLAlchemy (tested with version 0.9.8)
* Python database adapter for the database used
    - For MySQL: [mysql-python](https://pypi.python.org/pypi/MySQL-python) or [any other adapter supported by SQLAlchemy](http://docs.sqlalchemy.org/en/latest/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqldb)
    - For PostgreSQL: [psycopg2](http://pypi.python.org/pypi/psycopg2/) or [any other adapter supported by SQLAlchemy](http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2)

Database Configuration
----------------------

The database is configured in the xalt_db.conf file via a [connection string](http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html)

Example for MySQL with default adapter (mysql-python):

    [DATABASE]
    CONNECTION_STRING = mysql://testuser:testpassword@databasehost/databasename


Example for PostgreSQL with explicitly defined adapter:

    [DATABASE]
    CONNECTION_STRING = postgresql+psycopg2://testuser:testpassword@databasehost/databasename


Running the tests
-----------------

Tests for rudimentary functionality of the database classes are done by running 'make test', which in turn then run all
the Python unit tests in the test folder.

Examples
--------

Before you can communicate with the database through the orm you need to set up a session.
Sessions are not thread-safe. The changes done in a session can be commited to the database using 'session.commit()'
or can be rolled back using 'session.rollback()'.

```python
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine('mysql://testuser:testpassword@databasehost/databasename')
    Session = sessionmaker(bind=engine)

    session = Session()
```

The session should be closed after you are done with it using 'session.close()'

The following examples assume that a session has already been opened.

Saving an XALT_link object:

```python
    link_object = XALT_link(
        uuid = 'some uuid',
        hash_id = 'some hash',
        link_program = 'gcc',
        build_user = 'testuser',
        build_syshost = 'testhost',
        build_epoch = float('1234'),
        date = datetime.fromtimestamp(float(1234)),
        exit_code = 0,
        exec_path = '/home/testuser/testapp'
    )

    session.add(link_object)
    session.commit()
```

Querying for all XALT_link objects:

```python
link_objects = session.query(XALT_link).all()
```

Querying for all XALT_link objects with the uuid 'abc':

```python
link_objects = session.query(XALT_link).filter(XALT_link.uuid == 'abc').all()
```

Querying for all XALT_object objects with object_path '/test' and syshost 'testhost':

```python
from sqlalchemy import and_

db_obj = session.query(XALT_object).filter(and_(
                                    XALT_object.object_path == '/test',
                                    XALT_object.syshost ==  'testhost')).all()
```

Get the Top 10 modules for host 'testhost':

```python
from sqlalchemy import func
session.query(XALT_run.module_name, func.count(XALT_run.module_name)).filter(XALT_run.syshost == 'testhost').group_by(XALT_run.module_name).limit(10).all()
```

Execute raw SQL:

```python
rows = session.execute('SELECT * FROM XALT_run')
for row in rows:
    print row['date']
```