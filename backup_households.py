import json
import pco
import zipfile

from datetime import date
from urllib.parse import urlencode


HOUSEHOLDS_ENDPOINT = pco.PcoConfig.get('ENDPOINT', 'people_url') + '/households'


def get_households():
	api = pco.PcoEndpointApi('Household', HOUSEHOLDS_ENDPOINT)

	response = api.search()

	for household in response:

		# Move members out of relationships

		household['members'] = household['relationships']['people']['data']

		for member in household['members']:
			person = pco.PcoPerson.get(member['id'])

			member['name'] = person.name

		# Delete paths

		del(household['relationships'])
		del(household['links'])

	return response


def get_times(signup_id):
	times_endpoint = SIGNUPS_ENDPOINT + '/' + str(signup_id) + '/signup_times'

	api = pco.PcoEndpointApi('SignupTime', times_endpoint)

	response = api.search()

	for time in response:
		del(time['links'])

	return response


def main():

	# Pre-cache all people

	pco.PcoPerson.search()

	households_json = get_households()

	save(json.dumps(households_json, indent=2))


def save(file_content):
	base_filename = 'lcbc-people-households-' + date.today().strftime('%Y%m%d')

	internal_filename = base_filename + '.json'
	nonzip_filename = 'backups/' + base_filename + '.json'
	zip_filename = 'backups/' + base_filename + '.zip'

	#with zipfile.ZipFile(zip_filename, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
	#	zip_file.writestr(internal_filename, file_content)

	with open(nonzip_filename, 'w') as file:
		file.write(file_content)


if __name__ == '__main__':
	main()
