from . import api as pco_api


class PcoPerson():
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
		api = pco_api.PcoApi.get_instance()

		data = api.people.people.get(id)

		person = PcoPerson(data)

		return person

	def search(params={}):
		result = []

		api = pco_api.PcoApi.get_instance()

		data = api.people.people.search(params)

		for datum in data:
			person = PcoPerson(datum);

			result.append(person)

		return result
