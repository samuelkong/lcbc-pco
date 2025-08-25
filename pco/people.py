from . import api as pco_api
from . import cache


class PcoPerson():
	TYPE = 'Person'

	json = {}

	def __init__(self, json):
		self.json = json

	def __getattr__(self, name):
		if (name in self.json['attributes']):
			return self.json['attributes'][name]

		if (name == "id"):
			return self.json['id']

		return None

	def get(id):
		data = cache.PcoCache.get(PcoPerson.TYPE, id)

		if (data != None):
=			return PcoPerson(data)

		api = pco_api.PcoApi.get_instance()

		data = api.people.people.get(id)

		cache.PcoCache.put(data)

		return PcoPerson(data)

	def search(params={}):
		result = []

		api = pco_api.PcoApi.get_instance()

		data = api.people.people.search(params)

		for datum in data:
			cache.PcoCache.put(datum)

			person = PcoPerson(datum);

			result.append(person)

		return result
