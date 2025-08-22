import requests
import time

class PcoMeteredApi:
	request_rate_count = 0
	request_rate_limit = 100
	request_rate_period = 20

	def __init__(self, config):
		self.config = config
		self.client_id = config['DEFAULT']['client_id']
		self.secret = config['DEFAULT']['secret']


	def fetch(self, url):
		try:
			self.throttle()

			response = requests.get(url, auth=(self.client_id, self.secret))

			if self.reached_rate_limit(response):
				return self.fetch(url)

			response.raise_for_status()

			self.record_header(response)

			return response.json()
		except requests.exceptions.RequestException as e:
			print('ERROR:', e)

	def reached_rate_limit(self, response):
		if (response.status_code != requests.codes.too_many_requests):
			return False

		retry_after = response.headers['Retry-After']

		print('WARN: Reached rate limit. Waiting', retry_after, 'seconds.')

		time.sleep(retry_after)

		return TRUE

	def record_header(self, response):
		PcoMeteredApi.request_rate_count = int(response.headers['X-PCO-API-Request-Rate-Count'])
		PcoMeteredApi.request_rate_limit = int(response.headers['X-PCO-API-Request-Rate-Limit'])
		PcoMeteredApi.request_rate_period = int(response.headers['X-PCO-API-Request-Rate-Period'])

	def throttle(self):
		if PcoMeteredApi.request_rate_count < (PcoMeteredApi.request_rate_limit * 0.9):
			return

		rate_per_sec = PcoMeteredApi.request_rate_limit / PcoMeteredApi.request_rate_period
		rate_recovery_amount = 0.1 * PcoMeteredApi.request_rate_limit

		time_to_sleep = rate_recovery_amount / rate_per_sec

		print('WARN: Throttling: ' +
			  f'count={PcoMeteredApi.request_rate_count} ' +
			  f'limit={PcoMeteredApi.request_rate_limit} ' +
			  f'sleep={time_to_sleep}')

		time.sleep(time_to_sleep)