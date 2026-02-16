import argparse
import pco


def get_times(date):
	result = pco.PcoCheckIn.search(
		{
			'order': 'created_at',
			'where[created_at][gte]': date,
			'where[created_at][lte]': date
		}
	)

	for check_in in result:
		print(check_in.created_at)

	print(f'\nLen: {len(result)}')


def main():
	parser = argparse.ArgumentParser(
		prog='py get_check_in_times.py',
		formatter_class=argparse.RawTextHelpFormatter
	)

	parser.add_argument('date', help='YYYY-MM-DD')

	args = parser.parse_args()

	get_times(args.date)


if __name__ == '__main__':
	main()
