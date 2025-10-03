import pco
import re
import usaddress

from pco import config


ERROR_CODE_CITY = 'CT'
ERROR_CODE_COUNTRY = 'CO'
ERROR_CODE_POBOX_PO = 'BP'
ERROR_CODE_POBOX_BOX = 'BB'
ERROR_CODE_POBOX_ID = 'BI'
ERROR_CODE_STATE = 'ST'
ERROR_CODE_STREET_NUMBER = 'SN'
ERROR_CODE_STREET_SUFFIX = 'SS'
ERROR_CODE_STREET1 = 'S1'
ERROR_CODE_STREET2 = 'S2'
ERROR_CODE_ZIP = 'ZC'


def format_address(address):
	full_address = f'{address.street_line_1}, '

	if (not address.street_line_2 == None):
		full_address += f'{address.street_line_2}, '

	full_address += f'{address.city}, {address.state} {address.zip}'

	if ((not address.country_name == 'United States') or (address.country_name == None)):
		full_address += f' {address.country_name}'

	return full_address


def get_address_component(address_parts, label):
	for part in address_parts:
		if (part[1] == label):
			return part[0]

	return None


def is_pobox(address_parts):
	for part in address_parts:
		if (part[1] == 'USPSBoxType'):
			return True
		if (part[1] == 'USPSBoxID'):
			return True
	
	return False


def valid_street_number(address_parts):
	number = get_address_component(address_parts, 'AddressNumber')

	if (number == None):
		return False

	return number.isdecimal()


def valid_street_suffix(address_parts):
	suffix = get_address_component(address_parts, 'StreetNamePostType')

	if (suffix == None):
		return False
	if (suffix in config.PcoConfig.get('ADDRESS', 'street_suffix')):
		return True

	return False


def validate_city(city):
	if (city == None):
		return [ERROR_CODE_CITY]
	if (city in config.PcoConfig.get('ADDRESS', 'cities')):
		return []
	return [ERROR_CODE_CITY]


def validate_country(country):
	if (country == None):
		return [ERROR_CODE_COUNTRY]
	if (country in config.PcoConfig.get('ADDRESS', 'countries')):
		return []
	return [ERROR_CODE_COUNTRY]


def validate_pobox(address_parts):
	found_po = False
	found_box = False
	found_id = False

	for part in address_parts:
		if ((part[1] == 'USPSBoxType') and (part[0] == 'PO')):
			found_po = True
		if ((part[1] == 'USPSBoxType') and (part[0] == 'Box')):
			found_box = True
		if (part[1] == 'USPSBoxID'):
			found_id = True

	error_codes = []

	if (not found_po):
		error_codes += [ERROR_CODE_POBOX_PO]
	if (not found_box):
		error_codes += [ERROR_CODE_POBOX_BOX]
	if (not found_id):
		error_codes += [ERROR_CODE_POBOX_ID]

	return error_codes


def validate_state(state):
	if (state == None):
		return [ERROR_CODE_STATE]
	if (state in config.PcoConfig.get('ADDRESS', 'states')):
		return []
	return [ERROR_CODE_STATE]


def validate_street1(street1):
	if (street1 == None):
		return [ERROR_CODE_STREET1]

	address_parts = usaddress.parse(street1)

	if (is_pobox(address_parts)):
		return validate_pobox(address_parts)

	error_codes = []

	if (not valid_street_number(address_parts)):
		error_codes += [ERROR_CODE_STREET_NUMBER]

	if (not valid_street_suffix(address_parts)):
		error_codes += [ERROR_CODE_STREET_SUFFIX]

	if (not street1 == street1.strip()):
		error_codes += [ERROR_CODE_STREET1]
	#elif (not street1.istitle()):
	#	error_codes += [ERROR_CODE_STREET1]

	return error_codes


def validate_street2(street2):
	if (street2 == None):
		return []

	if (not street2 == street2.strip()):
		return [ERROR_CODE_STREET2]

	street2 = street2.strip()

	if (len(street2) <= 3):
		return [ERROR_CODE_STREET2]

	if (street2.isdecimal()):
		return [ERROR_CODE_STREET2]

	if (street2.startswith('Apt ') or
		street2.startswith('Unit ') or
		street2.startswith('PO Box ')):
		return []

	if (not street2.istitle()):
		return [ERROR_CODE_STREET2]

	return []


def validate_zip(zip):
	if (zip == None):
		return [ERROR_CODE_ZIP]

	pattern = r'^[0-9]{5}(-[0-9]{4})?$'

	if (re.fullmatch(pattern, zip)):
		return []

	return [ERROR_CODE_ZIP]


print('Ill-formed addresses:')

record_match_count = 0;

result = pco.PcoAddress.search()

for address in result:
	error_codes = []

	if (address.id in config.PcoConfig.get('IGNORES', 'check_address_ignore_ids')):
		continue

	error_codes += validate_street1(address.street_line_1)
	error_codes += validate_street2(address.street_line_2)
	error_codes += validate_city(address.city)
	error_codes += validate_state(address.state)
	error_codes += validate_zip(address.zip)
	error_codes += validate_country(address.country_name)

	if (len(error_codes) == 0):
		continue

	record_match_count += 1

	full_address = format_address(address)

	print(f'U:{address.person_id}\tA:{address.id}\t{','.join(error_codes)}\t{full_address}')

print(f'\nCount: {record_match_count}/{len(result)}')
