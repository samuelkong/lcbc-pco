import configparser


class PcoConfig():
	CONFIG_INI = 'config.ini'
	MY_CONFIG_INI = 'my_config.ini'

	config = None

	def get(section, option):
		if (PcoConfig.config == None):
			PcoConfig.init()

		return PcoConfig.config[section][option]

	def getList(section, option):
		comma_separated_str = PcoConfig.get(section, option)

		return [item.strip() for item in comma_separated_str.split(',')]

	def getboolean(section, option):
		return bool(PcoConfig.get(section, option))

	def getfloat(section, option):
		return float(PcoConfig.get(section, option))

	def getint(section, option):
		return int(PcoConfig.get(section, option))

	def init():
		PcoConfig.config = configparser.ConfigParser()

		PcoConfig.config.read([PcoConfig.CONFIG_INI, PcoConfig.MY_CONFIG_INI])
