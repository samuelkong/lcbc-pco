import pco


def is_title(household_name):
	name = household_name.replace(' Household', '')

	# Exception for names like McDonald

	if (not name.startswith('Mc')):
		return name.istitle()

	return name[2:].istitle()


print('Households with ill-formed names:')

record_match_count = 0;

result = pco.PcoHousehold.search()

for household in result:
	if (household.name.endswith('Household') and
		is_title(household.name) and
		household.name.isascii()):

		continue

	record_match_count += 1

	print(f'{household.id}\t{household.name}  ({household.primary_contact_name})')

print(f'\nCount: {record_match_count}/{len(result)}')
