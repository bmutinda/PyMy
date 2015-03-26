
class NoTableException(Exception):
	"""NoTableException"""
	def __init__(self, message='No table supplied'):
		super(NoTableException, self).__init__( message )
		self.message = message

class NoDataParamsException(Exception):
	"""NoDataParamsException"""
	def __init__(self, message='No data is supplied'):
		super(NoDataParamsException, self).__init__( message )
		self.message = message
		