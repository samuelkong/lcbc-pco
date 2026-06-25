import dataclasses
import dataclasses
import datetime
import csv
import random
import string


INPUT_REGISTRATION_CSV = 'vbs2026/vbs-2026-registration-20260618.csv'
OUTPUT_MANUAL_CHECKIN_CSV = 'vbs2026/manual-checkin-data.csv'


SECURITY_CODE_CHARS = [
	c for c in string.ascii_uppercase + string.digits
	if c not in 'IO10'
]


def add_security_code(attendees, column_name):
	codes = {}

	for attendee in attendees:
		reg_id = attendee['Registration ID']

		if reg_id not in codes:
			codes[reg_id] = ''.join(random.choices(SECURITY_CODE_CHARS, k=3))

		attendee[column_name] = codes[reg_id]

	return attendees


def get_attendees():
	with open(
		INPUT_REGISTRATION_CSV, encoding='utf-8', mode='r', newline=''
	) as file:
		attendees = list(csv.DictReader(file))

	return sorted(
		attendees,
		key=lambda attendee: (attendee['Last Name'], attendee['Registration ID'])
	)


def group_multiple_registration(attendees):
	registration_contacts = {}

	for attendee in attendees:
		key = (
			attendee['Registration Contact First Name'],
			attendee['Registration Contact Last Name'],
			attendee['Registration Contact Phone Number']
		)

		if key not in registration_contacts:
			registration_contacts[key] = attendee['Registration ID']
		elif registration_contacts[key] != attendee['Registration ID']:
			attendee['Registration ID'] = registration_contacts[key]

	return attendees


def main():
	attendees = get_attendees()

	attendees = group_multiple_registration(attendees)

	attendees = add_security_code(attendees, 'Security Code 1')
	attendees = add_security_code(attendees, 'Security Code 2')
	attendees = add_security_code(attendees, 'Security Code 3')
	attendees = add_security_code(attendees, 'Security Code 4')
	attendees = add_security_code(attendees, 'Security Code 5')

	save_manual_checkin_data(attendees)

	print(f"Total attendee: {len(attendees)}")



def save_manual_checkin_data(attendees):
	with open(
		OUTPUT_MANUAL_CHECKIN_CSV, encoding='utf-8', mode='w', newline=''
	) as file:
		writer = csv.writer(file)
		writer.writerow([
			'Last Name', 'First Name', 'Crew',
			'Security Code 1', 'Security Code 2', 'Security Code 3',
			'Security Code 4', 'Security Code 5'
		])
		for attendee in attendees:
			writer.writerow([
				attendee['Last Name'],
				attendee['First Name'],
				attendee['Assignment Area: Crews'],
				attendee['Security Code 1'],
				attendee['Security Code 2'],
				attendee['Security Code 3'],
				attendee['Security Code 4'],
				attendee['Security Code 5'],
			])


if __name__ == '__main__':
	main()
