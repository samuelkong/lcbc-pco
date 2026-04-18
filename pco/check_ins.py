from . import api as pco_api
from . import cache
from . import model


class PcoCheckIn(model.PcoBaseModel):
	TYPE = 'CheckIn'

	def __init__(self, json):
		super().__init__(json)

	@classmethod
	def api_get(clazz):
		return clazz.api.check_ins.check_ins.get

	@classmethod
	def api_search(clazz):
		return clazz.api.check_ins.check_ins.search
