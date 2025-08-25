import pco


def valid_first_name(first_name):
	if (first_name == None):
		return False
	if len(first_name) <= 1:
		return False
	if (not valid_name(first_name)):
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
	if ((len(name) > 1) and name.isupper()):
		return False
	return True


def valid_nickname(nickname):
	if (nickname == None):
		return True
	if (not nickname[0].isalpha() and nickname[0].islower()):
		return False
	if (nickname.isupper()):
		return False
	return True


print('Users with ill-formed names:')

data = pco.PcoPerson.search()

ill_form_count = 0;

for datum in data:
	if (valid_first_name(datum['attributes']['first_name']) and
		valid_last_name(datum['attributes']['last_name']) and
		valid_middle_name(datum['attributes']['middle_name']) and
		valid_given_name(datum['attributes']['given_name']) and
		valid_nickname(datum['attributes']['nickname'])):

		continue

	ill_form_count += 1

	full_name = datum['attributes']['first_name']

	if datum['attributes']['given_name'] != None:
		full_name += ' (' + datum['attributes']['given_name'] + ')'

	if datum['attributes']['nickname'] != None:
		full_name += ' "' + datum['attributes']['nickname'] + '"'

	if datum['attributes']['middle_name'] != None:
		full_name += ' ' + datum['attributes']['middle_name']

	full_name += ' ' + datum['attributes']['last_name']
	full_name += '    {' + datum['id'] + '}'

	print(full_name)

print(f'\nCount: {ill_form_count}/{len(data)}')
