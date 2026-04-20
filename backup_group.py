import json
import pco
import zipfile

from datetime import date
from urllib.parse import urlencode


EVENTS_ENDPOINT = pco.PcoConfig.get('ENDPOINT', 'groups_url') + '/events'
GROUP_TYPES_ENDPOINT = pco.PcoConfig.get('ENDPOINT', 'groups_url') + '/group_types'
GROUPS_ENDPOINT = pco.PcoConfig.get('ENDPOINT', 'groups_url') + '/groups'


def get_attendances(event_id):
	event_attendances_endpoint = EVENTS_ENDPOINT + '/' + str(event_id) + '/attendances'

	api = pco.PcoEndpointApi('Attendance', event_attendances_endpoint)

	response = api.search()

	for attendance in response:

		# Directly embed relationships.person

		person_id = attendance['relationships']['person']['data']['id']

		person = pco.PcoPerson.get(person_id)

		attendance['attended'] = attendance['attributes']['attended']
		attendance['role'] = attendance['attributes']['role']
		attendance['person_id'] = person_id
		attendance['person_name'] = person.name

		# Delete paths

		del(attendance['attributes'])
		del(attendance['id'])
		del(attendance['links'])
		del(attendance['relationships'])
		del(attendance['type'])

	return response


def get_events(group_id):
	group_events_endpoint = GROUPS_ENDPOINT + '/' + str(group_id) + '/events'

	api = pco.PcoEndpointApi('Event', group_events_endpoint)

	response = api.search()

	for event in response:
		event_id = event['id']

		# Delete paths

		del(event['links'])
		del(event['relationships'])

		# Add attendance

		event['attendances'] = get_attendances(event_id)

	return response


def get_group_types():
	group_types = {}

	api = pco.PcoEndpointApi('GroupType', GROUP_TYPES_ENDPOINT)

	response = api.search()

	for type in response:
		id = type['id']
		name = type['attributes']['name']

		group_types[id] = name

	return group_types


def get_groups():
	api = pco.PcoEndpointApi('Group', GROUPS_ENDPOINT)

	response = api.search({'where[archive_status]': 'include'})

	for group in response:
		group_id = group['id']

		# Delete links

		del(group['links'])

		# Change group type ID to group type name

		simplify_group_type(group)

		# Add group membership

		group['membership'] = get_members(group_id)

		# Add group events

		group['events'] = get_events(group_id)

	return response


def get_members(group_id):
	group_members_endpoint = GROUPS_ENDPOINT + '/' + str(group_id) + '/people'

	api = pco.PcoEndpointApi('Person', group_members_endpoint)

	response = api.search()

	for member in response:
		del(member['links'])

	return response


def main():

	# Pre-cache all people

	pco.PcoPerson.search()

	groups_json = get_groups()

	save(json.dumps(groups_json, indent=2))


def save(file_content):
	base_filename = 'lcbc-groups-' + date.today().strftime('%Y%m%d')

	internal_filename = base_filename + '.txt'
	zip_filename = 'backup/' + base_filename + '.zip'

	with zipfile.ZipFile(zip_filename, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
		zip_file.writestr(internal_filename, file_content)


def simplify_group_type(group_json):
	group_type_id = group_json['relationships']['group_type']['data']['id']

	group_json['group_type'] = GROUP_TYPES[group_type_id]

	del(group_json['relationships'])


if __name__ == '__main__':
	GROUP_TYPES = get_group_types()

	main()
