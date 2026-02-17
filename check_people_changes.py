import argparse
import csv
import os


def compare(old_people_db, new_people_db, settings):
	for id, new_person in new_people_db.items():
		if id not in old_people_db:
			print_name(new_person)
			print('\tNEW')

			continue

		old_person = old_people_db[id]

		del(old_people_db[id])

		name_printed = False

		for key, new_value in new_person.items():
			if (key not in old_person):
				continue

			# Ignore 'Updated At'
			if ((not settings.updated_at) and (key == 'Updated At')):
				continue

			# Ignore custom fields
			if ((not settings.custom) and ("::" in key)):
				continue

			old_value = old_person[key]

			if (new_value != old_value):
				if (not name_printed):
					print_name(new_person)
					name_printed = True

				print(f'\t{key}')
				print(f'\t\tOld: {old_value}')
				print(f'\t\tNew: {new_value}')

	for id, old_person in old_people_db.items():
		print_name(old_person)
		print('\tDELETED')

def load_csv(path):
	people_db = {}

	with open(path, encoding='utf-8', mode='r', newline='') as f:
		reader = csv.DictReader(f)

		for row in reader:
			person_id = row['Person ID']

			people_db[person_id] = row

	return people_db


def main():
	parser = argparse.ArgumentParser('py check_people.changes.py')

	parser.add_argument('--old', '-o', type=readable_file, required=True, help='Path to old file')
	parser.add_argument('--new', '-n', type=readable_file, required=True, help='Path to new file')
	parser.add_argument('--custom', '-c', action='store_true', help='Include custom fields')
	parser.add_argument(
		'--updated-at',
		'-u',
		action='store_true',
		help='Include changes to the Updated At timestamp'
	)

	args = parser.parse_args()

	old_people_db = load_csv(args.old)
	new_people_db = load_csv(args.new)

	print()

	compare(old_people_db, new_people_db, args)


def print_name(person):
	print(
		f"{person['First Name']} {person['Last Name']} ({person['Person ID']})"
	)


def readable_file(path):
	if not os.path.isfile(path):
		raise argparse.ArgumentTypeError(f"The file '{path}' does not exist or is not a file.")
	return path

if __name__ == '__main__':
	main()
