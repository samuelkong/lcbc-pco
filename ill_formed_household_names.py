import pco


print('Households with ill-formed names:')

record_match_count = 0;

result = pco.PcoHousehold.search()

for household in result:
	if (household.name.endswith('Household') and
		household.name.istitle() and
		household.name.replace(' ', '').isascii()):

		continue

	record_match_count += 1

	print(f'{household.name}  ({household.primary_contact_name})    {{{household.id}}}')


print(f'\nCount: {record_match_count}/{len(result)}')
