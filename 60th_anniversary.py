import csv
import json


INPUT_CHECKINS_CSV = '60th_anniversary/in-checkins-20260601.csv'
INPUT_GROUP_ATTENDANCE_CSV = '60th_anniversary/in-group-attendance-20260601.csv'
INPUT_GROUP_SMALLGROUP_CSV = '60th_anniversary/in-group-smallgroup-20260601.csv'
INPUT_HOUSEHOLDS_JSON = '60th_anniversary/in-households-20260601.json'
INPUT_PEOPLE_CSV = '60th_anniversary/in-people-20260601.csv'
OUTPUT_HOUSEHOLDS_CSV = '60th_anniversary/out-households-20260601.csv'


def get_households():
	people = get_people()

	with open(INPUT_HOUSEHOLDS_JSON, encoding='utf-8', mode='r') as file:
		household_data = json.load(file)

	household_member_ids = {
		member['id']
		for household in household_data
		for member in household['members']
	}

	for person in people:
		if person['Person ID'] in household_member_ids:
			continue

		full_name = f"{person['First Name']} {person['Last Name']}"

		household_data.append({
			'type': 'Household',
			'id': person['Person ID'],
			'attributes': {
				'avatar': '',
				'created_at': '',
				'member_count': 1,
				'name': f"{person['Last Name']} Household",
				'primary_contact_id': person['Person ID'],
				'primary_contact_name': full_name,
				'updated_at': '',
			},
			'members': [
				{
					'type': 'Person',
					'id': person['Person ID'],
					'name': full_name,
				},
			],
		})

	return household_data


def get_people():
	with open(INPUT_PEOPLE_CSV, encoding='utf-8', mode='r', newline='') as file:
		people = list(csv.DictReader(file))

	return [
		person for person in people
		if person['Membership'] != 'EVENT ATTENDEE'
	]


def get_person_congregations():
	with open(INPUT_PEOPLE_CSV, encoding='utf-8', mode='r', newline='') as file:
		return {
			person['Person ID']: person['Congregation :: Congregation']
			for person in csv.DictReader(file)
		}


def main():
	household_data = get_households()

	person_congregations = get_person_congregations()

	with open(
		INPUT_CHECKINS_CSV, encoding='utf-8', mode='r', newline=''
	) as file:
		checkin_person_ids = {row['Person ID'] for row in csv.DictReader(file)}

	with open(
		INPUT_GROUP_ATTENDANCE_CSV, encoding='utf-8', mode='r', newline=''
	) as file:
		group_attendance_person_ids = {
			row['Person ID'] for row in csv.DictReader(file)
		}

	with open(
		INPUT_GROUP_SMALLGROUP_CSV, encoding='utf-8', mode='r', newline=''
	) as file:
		smallgroup_person_ids = {
			row['Person ID'] for row in csv.DictReader(file)
		}

	for household in household_data:
		member_ids = {member['id'] for member in household['members']}

		household['has_checkins'] = bool(member_ids & checkin_person_ids)

		household['has_group_attendance'] = bool(
			member_ids & group_attendance_person_ids
		)

		household['in_en_smallgroup'] = bool(
			member_ids & smallgroup_person_ids
		)

		household['congregation'] = ''

		for member_id in member_ids:
			congregation = person_congregations.get(member_id, '')
			if congregation:
				household['congregation'] = congregation
				break

	save(household_data)

	print(f"Total households: {len(household_data)}")



def save(household_data):
	with open(
		OUTPUT_HOUSEHOLDS_CSV, encoding='utf-8', mode='w', newline=''
	) as file:
		writer = csv.writer(file)
		writer.writerow([
			'Household ID', 'Household Name', 'Household Size', 'Members',
			'Congregation', 'Looks Active', '5+ CheckIns',
			'5+ Group Attendance', 'EN SmallGroup',
		])

		for household in household_data:
			member_names = '\n'.join(
				member['name'] for member in household['members']
			)
			looks_active = (
				household['has_checkins']
				or household['has_group_attendance']
				or household['in_en_smallgroup']
			)
			writer.writerow([
				household['id'],
				household['attributes']['name'],
				household['attributes']['member_count'],
				member_names,
				household['congregation'],
				looks_active,
				household['has_checkins'],
				household['has_group_attendance'],
				household['in_en_smallgroup'],
			])


if __name__ == '__main__':
	main()
