from opencc import OpenCC

import pco


def remove_ascii(str):
	return ''.join(char for char in str if ord(char) > 127)

cc = OpenCC('s2t')

print('Users with name in simplified chinese:')

ill_form_count = 0;

result = pco.PcoPerson.search()

for person in result:
	full_name = person.first_name + ' ' + person.last_name

	name = remove_ascii(full_name)

	corrected_name = cc.convert(name)

	if (name == corrected_name):
		continue

	ill_form_count += 1


	print(f'{{{person.id}}}    {full_name} => {corrected_name}')

print(f'\nCount: {ill_form_count}/{len(result)}')
