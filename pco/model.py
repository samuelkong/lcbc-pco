from . import api as pco_api
from . import cache


class PcoBaseModel:
	TYPE = None

	api = pco_api.PcoApi.get_instance()

	def __getattr__(self, name):
		if (name in self.json['attributes']):
			return self.json['attributes'][name]

		if (name == 'id'):
			return self.json['id']

		return None

	def __init__(self, json):
		self.json = json

	@classmethod
	def api_get(clazz):
		print('Error: method not implemented')
		return None

	@classmethod
	def api_search(clazz):
		print('Error: method not implemented')
		return None

	@classmethod
	def get_type(clazz):
		return clazz.TYPE

	@classmethod
	def get(clazz, id):
		data = cache.PcoCache.get(clazz.TYPE, id)

		if (data != None):
			return clazz(data)

		data = clazz.api_get()(id)

		cache.PcoCache.put(data)

		return clazz(data)

	@classmethod
	def search(clazz, params={}):
		result = []

		data = clazz.api_search()(params)

		for datum in data:
			cache.PcoCache.put(datum)

			model = clazz(datum);

			result.append(model)

		return result
