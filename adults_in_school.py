import pco

print('Children with age-grade mismatch:')

count = 0

result = pco.PcoPerson.search({'where[child]': 'false'})


for person in result:
	if (person.grade == None):
		continue

	count += 1

	print(f'{person.name}, grade={person.grade}')

print(f'\nCount: {count}/{len(result)}')
