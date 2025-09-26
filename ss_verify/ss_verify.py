import csv
import sys

from datetime import date
from pathlib import Path


household_csv_filename = 'in/ss-check-ins.csv'
trusted_csv_filename = 'in/trusted-people.csv'

adult_tpl_filename = 'tpl/adult.html'
child_tpl_filename = 'tpl/child.html'
trusted_adult_tpl_filename = 'tpl/trusted-adult.html'

html_footer_filename = 'tpl/footer.html'
html_header_filename = 'tpl/header.html'

output_filename = 'out/out.html'


def format_birthdate(birthdate):
	if (isinstance(birthdate, date)):
		return birthdate.strftime('%b %d, %Y')


def format_grade(grade):
	if (grade == '0'):
		return 'K'

	if (grade == '1'):
		return '1st'

	if (grade == '2'):
		return '2nd'

	if (grade == '3'):
		return '3rd'

	return grade + 'th'


def str_to_bool(str):
	return str.lower() in ['1', 't', 'true', 'y', 'yes']


if (not Path(household_csv_filename).is_file()):
	print(
		f'Please add the file {household_csv_filename}. The file should be be a CSV ' +
		'export from a PCO People List'
	)

	sys.exit()

if (not Path(trusted_csv_filename).is_file()):
	print(
		f'Please add the file {trusted_csv_filename}. The file should be be a CSV with ' +
		'columns for Household ID, Person ID, First Name, Last Name, and Mobile Phone ' +
		'Number'
	)

	sys.exit()

households = {}

with open(household_csv_filename, encoding='utf-8', newline='') as household_csv_file:
	reader = csv.DictReader(household_csv_file)

	for row in reader:
		household_id = row['Household ID']

		if (household_id not in households):
			households[household_id] = {'adults': [], 'children': [], 'trusted': [] }

			households[household_id]['adults'] = []
			households[household_id]['children'] = []
			households[household_id]['trusted'] = []

		if (str_to_bool(row['Child'])):
			households[household_id]['children'].append(row)
		else:
			households[household_id]['adults'].append(row)

with open(trusted_csv_filename, encoding='utf-8', newline='') as trusted_csv_file:
	reader = csv.DictReader(trusted_csv_file)

	for row in reader:
		household_id = row['Household ID']

		if (household_id not in households):
			continue

		households[household_id]['trusted'].append(row)

output = ''

for household_id in households.keys():
	output += '<div class="household">'
	output += (
		'<div class="intro">Thank you for taking time to verify your household ' +
		'information. This information will help us ensure your child\'s safety. ' +
		'<b>Instructions:</b> If any information is incorrect, please cross it out ' +
		'and write in the correct value. If any required information is missing, ' +
		'please fill in that information. Return to helpers at the check-in ' +
		'station.</div>'
	)
	output += '<div class="section-children">'
	output += f'<h3>Children</h3>\n'

	with open(child_tpl_filename, encoding='utf-8') as child_tpl_file:
		child_tpl = child_tpl_file.read()

	for child in households[household_id]['children']:
		if ((child['Birthdate'] == '') and (child['Grade'] == '')):
			birthdate = '⚠️'
		elif ((child['Birthdate'] == '') and (child['Grade'] == '-1')):
			birthdate = '⚠️'
		elif (child['Birthdate'] == ''):
			birthdate = 'Optional'
		else:
			birthdate = date.fromisoformat(child['Birthdate'])

		if ((birthdate == '⚠️') and (child['Grade'] == '')):
			grade = '⚠️'
		elif ((birthdate == '⚠️') and (child['Grade'] == '-1')):
			grade = '⚠️'
		elif (birthdate == 'Optional'):
			grade = format_grade(child['Grade'])
		elif (birthdate >= date(2020, 9, 1) and (child['Grade'] == '')):
			grade = 'N/A'
		elif (birthdate >= date(2020, 9, 1) and (child['Grade'] == '-1')):
			grade = 'N/A'
		elif (birthdate < date(2020, 9, 1) and (child['Grade'] == '')):
			grade = '⚠️'
		elif (birthdate < date(2020, 9, 1) and (child['Grade'] == '-1')):
			grade = '⚠️'
		else:
			grade = format_grade(child['Grade'])

		birthdate = format_birthdate(birthdate)

		output += child_tpl.format(
			first_name=child['First Name'],
			last_name=child['Last Name'],
			gender=child['Gender'],
			birthdate=birthdate,
			grade=grade
		)

	output += '</div>'
	output += '<div class="section-adults">'
	output += f'<h3>Adults</h3>\n'

	with open(adult_tpl_filename, encoding='utf-8') as adult_tpl_file:
		adult_tpl = adult_tpl_file.read()

	for adult in households[household_id]['adults']:
		output += adult_tpl.format(
			first_name=adult['First Name'],
			last_name=adult['Last Name'],
			mobile_number=adult['Mobile Phone Number'],
			email=adult['Home Email']
		)

	output += '</div>'
	output += '<div class="section-trusted-people">'
	output += f'<h3>Trusted People</h3>\n'
	output += (
		'<div>Trusted people are people you authorize to check-in and pick-up your ' +
		'child. Please cross out anyone you want to remove and write in the name and ' +
		'mobile number of anyone you want to add (e.g., a grandparent). Adding trusted ' +
		'people is optional.</div>'
	)

	with open(trusted_adult_tpl_filename, encoding='utf-8') as trusted_adult_tpl_file:
		trusted_adult_tpl = trusted_adult_tpl_file.read()

	for trusted_adult in households[household_id]['trusted']:
		output += trusted_adult_tpl.format(
			first_name=trusted_adult['First Name'],
			last_name=trusted_adult['Last Name'],
			mobile_number=trusted_adult['Mobile Phone Number']
		)

	output += '</div>\n'
	output += '</div>\n'

with open(html_header_filename, encoding='utf-8') as header_file:
	header = header_file.read()
with open(html_footer_filename, encoding='utf-8') as footer_file:
	footer = footer_file.read()
with open(output_filename, mode='w', encoding='utf-8') as output_file:
	output_file.write(header + '\n' +output + '\n' + footer)

print(f'Output at {output_filename}')