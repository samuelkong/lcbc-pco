import argparse
import csv
import os

from datetime import date


## Takes a CSV file of children and a CSV file their parents (exported from PCO People List),
## matches parents with children, and
## returns a CSV file with the child's name, parent's name, parent's email, parent's phone.


def add_parent_info(children_db, parents_db):
	for id, child in children_db.items():
		child['Parent1 First Name'] = ''
		child['Parent1 Last Name'] = ''
		child['Parent1 Email'] = ''
		child['Parent1 Phone'] = ''

		child['Parent2 First Name'] = ''
		child['Parent2 Last Name'] = ''
		child['Parent2 Email'] = ''
		child['Parent2 Phone'] = ''

		parent1, parent2 = get_parents(parents_db, child['Household ID'])

		if (parent1 != None):
			child['Parent1 First Name'] = parent1['First Name']
			child['Parent1 Last Name'] = parent1['Last Name']
			child['Parent1 Email'] = get_emails(parent1)
			child['Parent1 Phone'] = get_phones(parent1)

		if (parent2 != None):
			child['Parent2 First Name'] = parent2['First Name']
			child['Parent2 Last Name'] = parent2['Last Name']
			child['Parent2 Email'] = get_emails(parent2)
			child['Parent2 Phone'] = get_phones(parent2)


def get_emails(person):
	emails = [person['Home Email'], person['Work Email'], person['Other Email']]

	return ";".join(email for email in emails if email)


def get_phones(person):
	phones = [
		person['Mobile Phone Number'], person['Home Phone Number'],
		person['Work Phone Number'], person['Other Phone Number']
	]

	return ";".join(phone for phone in phones if phone)


def get_parents(parents_db, household_id):
	parent1 = None
	parent2 = None

	for id, parent in parents_db.items():
		if (parent['Household ID'] == household_id):
			if (parent['Household Primary Contact'] == "TRUE"):
				parent1 = parent
			elif (parent2 == None):
				parent2 = parent
			else:
				print('Too many parents/guardians: ' + household_id)


	return (parent1, parent2)


def load_csv(path):
	people_db = {}

	with open(path, encoding='utf-8', mode='r', newline='') as f:
		reader = csv.DictReader(f)

		for row in reader:
			person_id = row['Person ID']

			people_db[person_id] = row

	return people_db


def main():
	parser = argparse.ArgumentParser('py get_parent_info.py')

	parser.add_argument(
		'--children', '-c', type=readable_file, required=True, help='Path to children CSV')
	parser.add_argument(
		'--parents', '-p', type=readable_file, required=True, help='Path to parent CSV')

	args = parser.parse_args()

	children_db = load_csv(args.children)
	parents_db = load_csv(args.parents)

	add_parent_info(children_db, parents_db)

	save(children_db)


def readable_file(path):
	if not os.path.isfile(path):
		raise argparse.ArgumentTypeError(f"The file '{path}' does not exist or is not a file.")
	return path


def save(children_db):
	filename = 'get-parent-info-' + date.today().strftime('%Y%m%d') + '.csv'

	with open(filename, 'w', encoding='utf-8') as file:
		csv_writer = csv.writer(file)

		csv_writer.writerow([
			'First Name', 'Last Name', 'Gender', 'Grade',
			'Parent1 First Name', 'Parent1 Last Name', 'Parent1 Email', 'Parent1 Phone',
			'Parent2 First Name', 'Parent2 Last Name', 'Parent2 Email', 'Parent2 Phone'
		])

		for id, child in children_db.items():
			csv_writer.writerow([
				child['First Name'],
				child['Last Name'],
				child['Gender'],
				child['Grade'],
				child['Parent1 First Name'],
				child['Parent1 Last Name'],
				child['Parent1 Email'],
				child['Parent1 Phone'],
				child['Parent2 First Name'],
				child['Parent2 Last Name'],
				child['Parent2 Email'],
				child['Parent2 Phone']
			])

	print('File saved to ' + filename)


if __name__ == '__main__':
	main()
