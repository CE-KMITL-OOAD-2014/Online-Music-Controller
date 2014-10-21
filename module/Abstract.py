from abc import ABCMeta, abstractmethod

class Command:
    __metaclass__ = ABCMeta
    @abstractmethod
    def execute(self):
        pass


class GetPlayerStatus():
	"""docstring for GetPlayerStatus"""
	__metaclass__ = ABCMeta    
	@abstractmethod
	def get_status(self) :
		pass