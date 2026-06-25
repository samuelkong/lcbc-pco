from . import api as pco_api
from . import cache
from . import model


class PcoGroup(model.PcoBaseModel):
	TYPE = 'Group'

	#def __getattr__(self, name):
	#	if (name == 'person_id'):
	#		return self.json['relationships']['person']['data']['id']

	#	return super().__getattr__(name)

	def __init__(self, json):
		super().__init__(json)

	@classmethod
	def api_get(clazz):
		return clazz.api.groups.groups.get

	@classmethod
	def api_search(clazz):
		return clazz.api.groups.groups.search
