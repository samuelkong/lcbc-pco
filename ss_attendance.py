import glob
import pandas


def main():
	attendance_df = pandas.DataFrame(columns=['First Name', 'Last Name', 'Grade'])

	for file in sorted(glob.glob('ss_attendance/attendance_reports/*.csv')):
		date = file[-25:-15]

		service1 = date + ' 09:00'
		service2 = date + ' 10:30'

		df = pandas.read_csv(file)

		df[[service1, service2]] = df['Location'].apply(split_location)

		df = df.drop(columns=['Location'])

		attendance_df = pandas.merge(
			attendance_df,
			df[['First Name', 'Last Name', 'Grade', service1, service2]],
			on=['First Name', 'Last Name', 'Grade'],
			how='outer',
		)

	attendance_df = attendance_df.fillna("")

	attendance_df.to_csv('ss_attendance/consolidated.csv', index=False, encoding='utf-8')


def split_location(location):
	services = ['', '']

	# Format: Location @ 9:00am
	# Format: Location @ 10:30am
	# Format: Location @ 9:00am and 10:30am

	locations = [location, location]

	# Format: Location @ 9:00am, Location @ 10:30am

	if (',' in location):
		locations[0],locations[1] = location.split(',', 1)

	for cur_location in locations:
		if ('9:00am' in cur_location):
			services[0] = cur_location
		if ('10:30am' in cur_location):
			services[1] = cur_location

	for i, service in enumerate(services):
		services[i] = service.split('@')[0].strip()


	return pandas.Series(services)


if __name__ == '__main__':
	main()
