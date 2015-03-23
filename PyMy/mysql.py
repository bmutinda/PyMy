__version__ = '1.0.0'
__author__ = 'Mutinda Boniface'
__website__ = 'http://mutindaz.github.io'
__description__ = 'Insanely easy python mysql query runner'

import MySQLdb

class MysqlConnector(object):
	def __init__( self ):
		self.db = None
		self.connected = False
		
	def connect( self, db_host, db_user, db_password, db_database ):
		self.db = None
		self.connected = False
		
		try:
			self.db = MySQLdb.connect( db_host, db_user, db_password, db_database )
			self.connected = True
		except MySQLdb.OperationalError, e:
			print 'MySQLdb -----> %s' %(str(e))
			raise e
			
		return self.db 
		
	def getConnection( self ):
		return self.db
		
	def disconnect( self ):
		if self.db:
			self.db.close()

		self.connected = False
		return True

	def isConnected( self ):
		return self.connected
	
	@staticmethod	
	def version( self ):
		return __version__ 
		
class QueryBuilder(object):
	def __init__( self, db ):
		self.db = db
		
	def run_query( self, query ):
		cursor = self.db.cursor( MySQLdb.cursors.DictCursor )
		cursor.execute( query )
		return cursor
		
	def run_insert( self, table, insert_data ):
		done = False
		keys = insert_data.keys()
		values = insert_data.values()
		query = "INSERT INTO %s (%s) VALUES  ('%s')" %(table, ",".join( keys ), "','".join( '%s' %x for x in values) )
		try:
			self.run_query(query)
			self.db.commit()
			done = True
		except Exception, e :
			self.db.rollback()
			raise e			
		return done	

	def run_select( self, table, what = '*', condition = None, limit = None ):
		what_data = ",".join( what )

		query = "SELECT %s FROM %s " %( what_data, table )
		# If their was a condition set we add it to our query	
		if condition:
			condition_keys = condition.keys()
			condition_values = condition.values()
			total_condition_data = len(condition_keys)
			if total_condition_data>0:
				query+=" WHERE "
				counter = 0
				separator = " AND "
				for key, val in condition.items():
					counter+=1
					if counter>=total_condition_data:
						separator = ""
					
					query+=' %s = \'%s\' %s' %(str(key), str(val), separator )

		if limit:
			query+=' LIMIT %s' %(str(limit))
		cursor = self.run_query( query )
		return cursor.fetchall()