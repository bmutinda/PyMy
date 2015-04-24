# Python MySQL Class
Easy to use MySQL database wrapper utility for python using MySQLdb package

### Dependencies 
MySQLdb - https://pypi.python.org/pypi/MySQL-python

### Downloading 
Download from git as a zip folder and extract its contents OR 
clone from git via ```git clone https://github.com/mutindaz/PyMy```

### Installation 
~ Copy the PyMy folder to your project folder then continue rocking... :)

### Getting started
See demo.py

### Quick Guide 
```python
from PyMy import MysqlConnector,QueryBuilder

# Database connection
conn = None 
sql = None 
try:
	conn = MysqlConnector.connect( '127.0.0.1', 'root', 'password', 'database' )
except Exception as dbe:
	print 'Database connection exception error ::%s' %(str(dbe))

# Build a query runner object using the obtained database connection 
# NB: This way makes it easy for someone to use more than one connection to run queries 
# as you can create instances of sql runner object from several connections 
# and use whichever you want to execute a query 
if conn:
	sql = QueryBuilder.build( conn )

""" Refer to the builder script for documentation about these methods """


""" Run a custom query : Returns cursor """
# Without params 
cursor = sql.run_query("select  now()")
cursor = sql.run_query("select * from services where status=%s AND name=%s", (0, "service_name") )


""" Insert in a table """
# Insert as a context - returns the row id 
inserted = sql.run_insert('services', {'name': 'service name here', 'description': 'service description here'})
inserted2 = sql.run_insert('services', {'name': 'service name here', 'description': 'service description here'}, "REPLACE")


""" Run a select query """
# Params as string  
data = sql.run_select('services', "status,date_created", "status=0" )
data = sql.run_select('services', ('status','date_created'), {'status':0}, 'date_created DESC', 12 )


""" 
Run an update query  
NB: data and condition can be str or dict 
"""
updated = sql.run_update('services', {"status":0, "name":'services'}, None )
updated = sql.run_update('services', {"status":0, "name":'services'}, {"status": 0} )

"""
Run delete query 
"""
deleted = sql.run_delete('services')
deleted = sql.run_delete('services', "status = 0")

```
