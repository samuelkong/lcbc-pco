from . import request

class PcoPerson(request.PcoMeteredApi):
	json = {}

	def __init__(self, config, json):
		super().__init__(config)

		self.json = json

	def __getattr__(self, name):
		if (name in self.json['attributes']):
			return self.json['attributes'][name]
		return None
