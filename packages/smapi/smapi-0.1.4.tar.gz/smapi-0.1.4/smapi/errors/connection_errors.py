class SteamConnectionError(Exception):
	"""Raises when response code isn't 200"""
	pass


class SteamBadRequestError(Exception):
	"""Raises if total count of items is 0 or if response is unsuccessful"""

	def __init__(self, url, query):
		super(SteamBadRequestError, self).__init__(
				'\n'
				f'Not even one lot was found by this link or name - "{url}"\n'
				f'Maybe something wrong with your query - "{query}"'
		)


class CSGOFloatConnectionError(Exception):
	"""Raises when response code isn't 200"""
	pass
