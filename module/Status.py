from Abstract import GetPlayerStatus

class ControlStatus(GetPlayerStatus):
	"""docstring for ControlStatus"""
	def get_status(self,address):
		return "get Control status"

class MemoryStatus(GetPlayerStatus):
	"""docstring for ControlStatus"""
	def get_status(self,address):
		return "get Memory status"		
		
