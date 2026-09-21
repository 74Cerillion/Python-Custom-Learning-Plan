"""SQLite vs sqlite3
SQLite is the actual DB engine
    Relational DB Management system that doesn't normally have a separate DB server somewhere external waiting for a connection
    Python Program -> SQLite Engine -> Database.db
    DB can be tiny, local, disposable, and deterministic
sqlite3 is Python's interfae to SQLite
    My Python -> sqlite3 -> SQLite -> DB
SQLite is the engine, sqlite3 is the interface, and the .db is the file where SQLite durably stores state
"""

"""Connections
Temporary local connection to the SQLite DB. Different from web or network (HTTP) Conncetions because it's local
"""

"""Cursors
Operates alongside connection to manage individual stream of SQL operations and their results
Actually performs operations on the connection
    cursor.execute(SELECT x FROM y WHERE z)
Connection can do this too, but cursor is the standard
"""

"""execute()
See Cursor notes for usage
    Method that actually takes and executes the SQL statement
cursor.execute(INSERT.........)
"""

"""Parameterized Queries"""
cursor.execute(
    "INSERT ... VALUES (?, ?)",
    (symbol, price)
)
#Important because normal insertions, whilst functional, open vulnerabilities
#You allow values to be executed as code, which opens the door to injection attacks

"""Database Files vs :memory:
:memory: allows you to create a SQLite DB in memory, so that once the program/state goes away, the DB goes with not
    This is, obviously, neither durable nor persistent
Useful for testing, usually not for implementation
"""

"""commit()
Sort of like github, once a statement has been ran it is executed(()), but it has not been saved yet.
This crucial detail allows for idempotency, because you can now run multiple commands before 'hitting save',
    and roll back if command 17 fails.
So persistence, then, becomes the idea that information will survive program termination
Durability becomes the guarantee that comes after the successful commit.
Persistence is the idea that our program can survive termination, durability is the idea that once we have
    committed to a transaction, the transaction will survive program/DB termination.
Where you commit says "This point constitutes one completed unit of work"
"""

"""Transactions
A group of transactions treated as one logical unit of work. Either the transaction completes as a unit or its changes
    do not become durable.
"""

"""rollback()
Abandons uncommitted changes in current transaction
    So if the transaction completes 5 executions, and all 5 need to exist for it be valid, then we run a commit after 5.
    But now what if execution 4 fails?
    We rollback() to before the transaction began, and retry. We don't proceed then commit()
ROLLBACK ONLY WORKS WITH UNCOMMITTED CHANGES
"""

"""sqlite3.IntegrityError
Python's custom exception indicating that SQLite rejected an operation because it would violate an integrity constraint
    ex. You try to perform an INSERT that violates uniqueness on the Composite Key, you will get this error
"""

"""Context Managers
General idea is to enter a managed context, perform work, and guarantee defined cleanup/exit behvaior when that
    context ends - even if an exception occurs
ex.
Acquire lock
     │
     ▼
critical operation
     │
     ▼
Release lock
"""