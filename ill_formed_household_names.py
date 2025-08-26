import pco


print('Households with ill-formed names:')

ill_form_count = 0;

result = pco.PcoHousehold.search()

for household in result:
	if (household.name.endswith('Household') and
		household.name.istitle() and
		household.name.replace(' ', '').isascii()):

		continue

	ill_form_count += 1

	print(f'{household.name}  ({household.primary_contact_name})    {{{household.id}}}')


print(f'\nCount: {ill_form_count}/{len(result)}')
