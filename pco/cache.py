class PcoCache:
	cache = {}

	def get(type, id):
		id = str(id)

		if (type not in PcoCache.cache):
			return None

		if (id not in PcoCache.cache[type]):
			return None

		return PcoCache.cache[type][id]

	def put(data):
		type = data['type']
		id = data['id']

		if (type not in PcoCache.cache):
			PcoCache.cache[type] = {}

		PcoCache.cache[type][id] = data

