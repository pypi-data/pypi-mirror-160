from typing import Dict, Union
import requests


class _DataFetcher(object):

	@staticmethod
	def _get_page(link: str, user_agent: str, params: Dict['str', Union[str, int]] = None):
		if not (isinstance(link, str) and
		        isinstance(user_agent, str) and
		        isinstance(params, dict)):
			raise TypeError

		response = requests.get(link, params=params, headers={'user-agent': user_agent})

		if not response.status_code == 200:
			raise ConnectionError

		return response

	def _get_json(self, link: str, user_agent: str, params: Dict['str', Union[str, int]] = None) -> Dict[
		str, Union[str, int]]:
		if not (isinstance(link, str) and
		        isinstance(params, dict)):
			raise TypeError

		response = self._get_page(link, user_agent, params)
		return response.json()

	def get_steam_market_page(self, url: str, user_agent: str, __filter: str, language: str,
	                          currency: str, start: int, count: int) -> Dict[str, Union[str, int]]:
		if not (isinstance(url, str) and
		        isinstance(user_agent, str) and
		        isinstance(__filter, str) and
		        isinstance(language, str) and
		        isinstance(currency, str) and
		        isinstance(start, int) and
		        isinstance(count, int)):
			raise TypeError

		market_listing_base = 'https://steamcommunity.com/market/listings/730/'

		if market_listing_base not in url:
			url = market_listing_base + url
		elif market_listing_base.replace('730/', '') in url and '730' not in url:
			raise RuntimeError

		link = f'{url}/render/'

		return self._get_json(link, user_agent, params={
				'filter': __filter, 'start': start, 'count': count,
				'language': language, 'currency': currency
		})

	def get_float_api_page(self, lookup_link: str, user_agent: str, custom_link: str = ''):
		if not (isinstance(lookup_link, str) and
		        isinstance(user_agent, str) and
		        isinstance(custom_link, str)):
			raise TypeError

		if not custom_link == '':
			link = custom_link
		else:
			link = 'https://api.csgofloat.com/'

		return self._get_json(link, user_agent, params={
				'url': lookup_link
		})
