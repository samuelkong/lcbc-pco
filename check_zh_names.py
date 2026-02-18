from opencc import OpenCC

import pco


def main():
	cc = OpenCC('s2t')

	print('People with name in simplified Chinese:')

	record_match_count = 0;

	result = pco.PcoPerson.search()

	for person in result:
		full_name = person.first_name + ' ' + person.last_name

		name = remove_ascii(full_name)

		converted_name = cc.convert(name)

		if (name == converted_name):
			continue

		record_match_count += 1

		print(f'{person.id}\t{full_name}  =>  {converted_name}')

	print(f'\nCount: {record_match_count}/{len(result)}')


def remove_ascii(str):
	return ''.join(char for char in str if ord(char) > 127)


if __name__ == '__main__':
	main()
