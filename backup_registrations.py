import json
import pco
import zipfile

from datetime import date
from urllib.parse import urlencode


SIGNUPS_ENDPOINT = pco.PcoConfig.get('ENDPOINT', 'registrations_url') + '/signups'


def get_location(signup_id):
	location_endpoint = SIGNUPS_ENDPOINT + '/' + str(signup_id) + '/signup_location'

	api = pco.PcoEndpointApi('SignupLocation', location_endpoint)

	response = api.search()

	if (response == {}):
		return response

	del(response['links'])

	return response


def get_signups():
	api = pco.PcoEndpointApi('Signup', SIGNUPS_ENDPOINT)

	response = api.search()

	for signup in response:
		signup_id = signup['id']

		# Add group membership

		signup['signup_location'] = get_location(signup_id)

		# Add times

		signup['signup_times'] = get_times(signup_id)

		# Delete paths

		del(signup['links'])

	return response


def get_times(signup_id):
	times_endpoint = SIGNUPS_ENDPOINT + '/' + str(signup_id) + '/signup_times'

	api = pco.PcoEndpointApi('SignupTime', times_endpoint)

	response = api.search()

	for time in response:
		del(time['links'])

	return response


def main():
	signups_json = get_signups()

	save(json.dumps(signups_json, indent=2))


def save(file_content):
	base_filename = 'lcbc-registrations-' + date.today().strftime('%Y%m%d')

	internal_filename = base_filename + '.txt'
	zip_filename = 'backup/' + base_filename + '.zip'

	with zipfile.ZipFile(zip_filename, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
		zip_file.writestr(internal_filename, file_content)


if __name__ == '__main__':
	main()
