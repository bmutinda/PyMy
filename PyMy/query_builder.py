import MySQLdb
from .exceptions import NoTableException, NoDataParamsException

class QueryBuilder(object):
	def __init__( self, db ):
		self.db = db

	@staticmethod
	def build( db_conn ):
		"""
		Creates and returns a new query runner object 
		"""
		return QueryBuilder(db_conn )

	def _dict_to_string( self, dict_data, separator = "AND"):
		if type(dict_data) is dict:
			query = ""
			data_list = []
			for key, value in dict_data.iteritems():
				data_list.append( '%s = \'%s\'' %(key, self.escape_string(value) ) )
			return (' %s ' %(separator)).join( data_list )

		return ""

	def escape_string( self, string):
		"""
		Creates an sql safe param
		"""
		return MySQLdb.escape_string( str(string) )
		
	def run_query( self, query, params=None ):
		"""
		Run a custom query
			{method} : run_query(query)
		params:
			@query - type(str) : the query to execute 
		"""
		if not self.db:
			raise 'It seems there is no active connection to MySQL'
		cursor = self.db.cursor( MySQLdb.cursors.DictCursor )
		cursor.execute( query , params)
		return cursor

	def run_insert( self, table, data, context = 'INSERT'):
		"""
		Run an insert query 
			{method} : run_insert( table, data, context )
		params:
			@table - type(str) : The table name to insert data to 
			@data - type(dict) : an associative array of key=>value combinations
			@context - type(str): the type of the query: INSERT/ REPLACE
		"""
		_required_context = ('INSERT', 'REPLACE')
		done = False
		if context.upper() in _required_context and table and data and context:
			if type(data) is dict:
				keys = data.keys()
				values = data.values()
				query = "%s INTO %s (%s) VALUES  ('%s')" %(context, table, ",".join( keys ), "','".join( '%s' %self.escape_string(x) for x in values) )
				try:
					self.run_query(query)
					self.db.commit()
					done = True
				except Exception, e :
					self.db.rollback()
					raise e	
		return done	

	def run_select( self, table, what = '*', condition = None, order_by=None, limit = None ):
		"""
		Run select query, Returns data as a associative array of key=>value
			{method} : run_select(table, what, filter, order_by, limit )
		params:
			@table 	- type(str): The table name to run query in 
			@filter - type(str, dict): The filter values,
				~ Can be either string or dict of key=>value combinations
			@order_by - type(str, dict): Order by params.
				~ Can be either string or dict of key=>value combinations
			@limit - type(int, str, tuple) The limit values
				~ Can be an int specifying the maximum number of rows or 
				 a string of start and max rows or a tuple of start and count 
		"""
		what_data = "*"
		if what:
			if type(what) is tuple:
				what_data = ",".join( what )
			elif type(what) is str:
				what_data = what

		query = "SELECT %s FROM %s " %( what_data, table )
		if condition:
			if type(condition) is dict:
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
						query+=' %s = \'%s\' %s' %(str(key), self.escape_string(val), separator )
			elif type(condition) is str:
				query+="WHERE %s" %(condition)

		if order_by:
			if type(order_by) is str:
				query+=' ORDER BY %s' %(order_by)
		if limit:
			if type(limit) is str or type(limit) is int:
				query+=' LIMIT %s' %(limit)
			elif type(limit) is tuple:
				query+=' LIMIT %s' %( ",".join(limit))

		cursor = self.run_query( query )
		return cursor.fetchall()


	def run_update( self, table, data, condition = None ):
		if not table or not type(table) is str:
			raise NoTableException()
		if not data:
			raise NoDataParamsException() 

		done = False 
		query = "UPDATE %s " %(table)
		if type(data) is str:
			query+='SET %s' %(data)
		elif type(data) is dict:
			data_string = self._dict_to_string( data, ",")
			query+="SET %s" %( data_string ) if data_string else ''

		if condition:
			if type(condition) is str:
				query+=" WHERE %s" %(condition)
			elif type(condition) is dict:
				data_string = self._dict_to_string( condition )
				query+=" WHERE %s" %( data_string ) if data_string else ''

		try:
			self.run_query(query)
			self.db.commit()
			done = True
		except Exception, e :
			self.db.rollback()
			raise e	
		return done 

	def run_delete( self, table, condition =None ):
		if not table or not type(table) is str:
			raise NoTableException()

		query = "DELETE FROM %s " %(table)
		if condition:
			if type(condition) is str:
				query+=" WHERE %s" %(condition)
			elif type(condition) is dict:
				data_string = self._dict_to_string( condition )
				query+=" WHERE %s" %( data_string ) if data_string else ''
		
		done = False
		try:
			self.run_query(query)
			self.db.commit()
			done = True
		except Exception, e :
			self.db.rollback()
			raise e	
		return done 
