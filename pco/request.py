import requests
import time


class PcoRequest:
	request_rate_count = 0
	request_rate_limit = 100
	request_rate_period = 20

	def get(url):
		try:
			PcoRequest.throttle()

			response = requests.get(url, auth=(PcoRequest.client_id, PcoRequest.secret))

			if (PcoRequest.reached_rate_limit(response)):
				return PcoRequest.fetch(url)

			response.raise_for_status()

			PcoRequest.record_header(response)

			return response.json()
		except requests.exceptions.RequestException as e:
			print('ERROR:', e)

	def init(client_id, secret):
		PcoRequest.client_id = client_id
		PcoRequest.secret = secret

	def reached_rate_limit(response):
		if (response.status_code != requests.codes.too_many_requests):
			return False

		retry_after = response.headers['Retry-After']

		print('WARN: Reached rate limit. Waiting', retry_after, 'seconds.')

		time.sleep(retry_after)

		return TRUE

	def record_header(response):
		PcoRequest.request_rate_count = int(
			response.headers['X-PCO-API-Request-Rate-Count'])
		PcoRequest.request_rate_limit = int(
			response.headers['X-PCO-API-Request-Rate-Limit'])
		PcoRequest.request_rate_period = int(
			response.headers['X-PCO-API-Request-Rate-Period'])

	def throttle():
		if (PcoRequest.request_rate_count < (PcoRequest.request_rate_limit * 0.85)):
			return

		rate_per_sec = PcoRequest.request_rate_limit / PcoRequest.request_rate_period
		rate_recovery_amount = 0.15 * PcoRequest.request_rate_limit

		time_to_sleep = rate_recovery_amount / rate_per_sec

		print(
			f'WARN: Throttling: count={PcoRequest.request_rate_count} ' +
			f'limit={PcoRequest.request_rate_limit} sleep={time_to_sleep}'
		)

		time.sleep(time_to_sleep)