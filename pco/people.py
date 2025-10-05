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


class PcoAddress(PcoBaseModel):
	TYPE = 'Person'

	def __getattr__(self, name):
		if (name == 'person_id'):
			return self.json['relationships']['person']['data']['id']

		return super().__getattr__(name)

	def __init__(self, json):
		super().__init__(json)

	@classmethod
	def api_get(clazz):
		return clazz.api.people.addresses.get

	@classmethod
	def api_search(clazz):
		return clazz.api.people.addresses.search


class PcoHousehold(PcoBaseModel):
	TYPE = 'Household'

	def __init__(self, json):
		super().__init__(json)

	@classmethod
	def api_get(clazz):
		return clazz.api.people.households.get

	@classmethod
	def api_search(clazz):
		return clazz.api.people.households.search


class PcoPerson(PcoBaseModel):
	TYPE = 'Person'

	def __init__(self, json):
		super().__init__(json)

	@classmethod
	def api_get(clazz):
		return clazz.api.people.people.get

	@classmethod
	def api_search(clazz):
		return clazz.api.people.people.search


class PcoPhoneNumber(PcoBaseModel):
	TYPE = 'PhoneNumber'

	def __getattr__(self, name):
		if (name == 'person_id'):
			return self.json['relationships']['person']['data']['id']

		return super().__getattr__(name)

	def __init__(self, json):
		super().__init__(json)

	@classmethod
	def api_get(clazz):
		return clazz.api.people.phone_numbers.get

	@classmethod
	def api_search(clazz):
		return clazz.api.people.phone_numbers.search
