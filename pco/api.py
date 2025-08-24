from . import config
from . import request
from urllib.parse import urlencode


class PcoApi():
	def __init__(self):
		products = [
		#	'calendar',
			'check_ins',
		#	'giving',
		#	'groups',
			'people',
		#	'publishing',
		#	'registrations',
		#	'services'
		]

		for product in products:
			setattr(self, product, PcoProductApi(product))


class PcoEndpointApi():
	def __init__(self, name, url):
		self.name = name
		self.url = url

	def get(self, id):
		response = request.PcoRequest.get(self.url + '/' + str(id))

		return response['data']

	def search(self, params={}, return_all=True):
		if return_all == True:
			params['per_page'] = config.PcoConfig.get('REQUEST', 'max_page_size')

		query = urlencode(params)

		response = request.PcoRequest.get(self.url + '?' + query)

		response_data = response['data']

		if (return_all == True) and ('next' in response['meta']):
			params['offset'] = response['meta']['next']['offset']

			next_response_data = self.search(params, return_all)

			response_data = response_data + next_response_data

		return response_data


class PcoProductApi():
	def __init__(self, product):
		self.name = product;

		links = self.get_links()

		self.add_endpoints(links)

	def add_endpoints(self, links):
		for name, url in links.items():
			if url is None:
				continue

			if name == 'self':
				continue

			setattr(self, name, PcoEndpointApi(name, url))

	def get_links(self):
		if hasattr(self, 'links'):
			return self.links

		endpoint = config.PcoConfig.get('ENDPOINT', self.name + '_url')

		response = request.PcoRequest.get(endpoint)

		self.links = response['data']['links']

		return self.links


def api():
	return PcoApi()
