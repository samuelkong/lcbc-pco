import pco


def format_full_name(person):
	full_name = person.first_name

	if (person.given_name != None):
		full_name += f' ({person.given_name})'

	if (person.nickname != None):
		full_name += f' "{person.nickname}"'

	if (person.middle_name != None):
		full_name += f' {person.middle_name}'

	full_name += f' {person.last_name}'

	return full_name


def valid_first_name(first_name):
	if (first_name == None):
		return False

	# Exception for names like O'Brian

	if (first_name[0:2] == "O'"):
		return valid_first_name(first_name[2:])

	if (not valid_name(first_name)):
		return False
	if (first_name.find('"') >= 0):
		return False
	if (first_name.find("'") >= 0):
		return False
	return True


def valid_given_name(given_name):
	if (given_name == None):
		return True
	if (len(given_name) <= 1):
		return False
	if (not valid_name(given_name)):
		return False
	return True


def valid_last_name(last_name):
	return valid_first_name(last_name)


def valid_middle_name(middle_name):
	if (middle_name == None):
		return True
	if (not valid_name(middle_name)):
		return False
	return True


def valid_name(name):
	if (not name[0].isalpha()):
		return False
	if (name[0].islower()):
		return False

	# Exception for initials followed by a period

	if ((len(name) == 2) and (name[1] == '.')):
		return True

	if ((len(name) > 1) and name.isupper()):
		return False
	return True


def valid_nickname(nickname):
	return True


print('People with ill-formed names:')

record_match_count = 0;

result = pco.PcoPerson.search()

for person in result:
	if (valid_first_name(person.first_name) and
		valid_last_name(person.last_name) and
		valid_middle_name(person.middle_name) and
		valid_given_name(person.given_name) and
		valid_nickname(person.nickname)):

		continue

	record_match_count += 1

	full_name = format_full_name(person)

	print(f'{person.id}\t{full_name}')

print(f'\nCount: {record_match_count}/{len(result)}')
