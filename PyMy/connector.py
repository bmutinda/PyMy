__version__ = '1.0.0'
__author__ = 'Mutinda Boniface'
__website__ = 'http://mutindaz.github.io'
__description__ = 'Insanely easy python MySQL query runner'

import MySQLdb

class MysqlConnector(object):
	def __init__( self ):
		self.db = None
		self.connected = False
	
	@staticmethod
	def connect( db_host, db_user, db_password, db_database ):
		return MysqlConnector()._doConnect( db_host, db_user, db_password, db_database )

	def _doConnect( self, db_host, db_user, db_password, db_database ):
		self.db = None
		self.connected = False
		try:
			self.db = MySQLdb.connect( db_host, db_user, db_password, db_database )
			self.connected = True
		except MySQLdb.OperationalError, e:
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