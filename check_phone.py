import pco
import re


ERROR_CODE_COUNTRY = 'CO'
ERROR_CODE_DUPLICATE = 'DD'
ERROR_CODE_NUMBER = 'PH'


seen_phones = set()


def get_fullname(person_id):
	person = pco.PcoPerson.get(person_id)

	return person.name


def is_duplicate(phone):
	code = (phone.person_id, phone.e164)

	if (code in seen_phones):
		return True

	seen_phones.add(code)

	return False


def valid_country(country_code):
	if (country_code == 'US'):
		return True
	return False


def valid_phone_number(national_number):
	if (national_number == None):
		return False

	pattern = r'^\(\d{3}\) \d{3}-\d{4}$'

	return re.fullmatch(pattern, national_number)


print('Problematic phone numbers:')
print('User ID\tUser Name\tPhone ID\tErrors\tPhone Number')

record_match_count = 0;

result = pco.PcoPhoneNumber.search()

for phone in result:
	error_codes = []

	if (not valid_country(phone.country_code)):
		error_codes += [ERROR_CODE_COUNTRY]

	if (is_duplicate(phone)):
		error_codes += [ERROR_CODE_DUPLICATE]

	if (not valid_phone_number(phone.national)):
		error_codes += [ERROR_CODE_NUMBER]

	if (len(error_codes) == 0):
		continue

	record_match_count += 1

	print(
		f'{phone.person_id}\t{get_fullname(phone.person_id)}\t{phone.id}\t' +
		f'{','.join(error_codes)}\t{phone.national}'
	)

print(f'\nCount: {record_match_count}/{len(result)}')
print()
print('Check phone type at https://www.phonevalidator.com/')