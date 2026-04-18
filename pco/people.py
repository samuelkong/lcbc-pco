from . import api as pco_api
from . import cache
from . import model


class PcoAddress(model.PcoBaseModel):
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


class PcoHousehold(model.PcoBaseModel):
	TYPE = 'Household'

	def __init__(self, json):
		super().__init__(json)

	@classmethod
	def api_get(clazz):
		return clazz.api.people.households.get

	@classmethod
	def api_search(clazz):
		return clazz.api.people.households.search


class PcoPerson(model.PcoBaseModel):
	TYPE = 'Person'

	def __init__(self, json):
		super().__init__(json)

	@classmethod
	def api_get(clazz):
		return clazz.api.people.people.get

	@classmethod
	def api_search(clazz):
		return clazz.api.people.people.search


class PcoPhoneNumber(model.PcoBaseModel):
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
