from . import request

class PcoPerson():
	json = {}

	def __init__(self, json):
		self.json = json

	def __getattr__(self, name):
		if (name in self.json['attributes']):
			return self.json['attributes'][name]
		return None
