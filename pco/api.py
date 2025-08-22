from . import request
from urllib.parse import urlencode

class PcoApi():
	def __init__(self, config):
		#products = [ 'calendar', 'check_ins', 'giving', 'groups', 'people', 'publishing',
		#			  'registrations', 'services' ]
		products = ['check_ins', 'people']

		for product in products:
			setattr(self, product, PcoProductApi(config, product))

class PcoEndpointApi(request.PcoMeteredApi):
	def __init__(self, config, name, url):
		super().__init__(config)

		self.name = name
		self.url = url

	def get(self, id):
		response = self.fetch(self.url + '/' + str(id))

		return response['data']

	def search(self, params, return_all=False):
		if return_all == True:
			params['per_page'] = self.config['DEFAULT']['max_page_size']

		query = urlencode(params)

		response = self.fetch(self.url + '?' + query)

		response_data = response['data']

		if (return_all == True) and ('next' in response['meta']):
			params['offset'] = response['meta']['next']['offset']

			next_response_data = self.search(params, return_all)

			response_data = response_data + next_response_data

		return response_data

class PcoProductApi(request.PcoMeteredApi):
	def __init__(self, config, product):
		super().__init__(config)

		self.name = product;

		links = self.get_links()

		self.add_endpoints(links)

	def add_endpoints(self, links):
		for name, url in links.items():
			if url is None:
				continue

			if name == 'self':
				continue

			setattr(self, name, PcoEndpointApi(self.config, name, url))

	def get_links(self):
		if hasattr(self, 'links'):
			return self.links

		endpoint = self.config['ENDPOINT'][self.name + '_url']

		response = self.fetch(endpoint)

		self.links = response['data']['links']

		return self.links

def api(config):
	return PcoApi(config)
