from typing import Any, Union, List, Dict
from dataclasses import asdict
from .data_handlers import *
from .info import *
import asyncio


class SteamMarketHandler:
	"""The class that provides you to automatize using of Community Market in Steam for CSGO the game."""

	def __init__(self, url: str, user_agent: str = '', custom_csgo_float: str = '', quantity: int = 0, query: str = '',
	             language: _Locale = Locales.US, currency: _Currency = Currencies.USD, do_first_search: bool = True):
		"""Initializer of Steam Market Handler class
		
		:param str url: Link to listing in Steam Community Market, also can contain name of your weapon like an
		"AK-47 | Vulcan (Field-Tested)", only in english
		:param str user_agent: User agent for data gathering from internet, leave empty for using default value of it
		:param str custom_csgo_float: Custom address to CSGO Float Api, in case if you are hosting this api yourself
		:param int quantity: Count of all lots that will be parsed, leave 0 to parse all items
		:param str query: Specified filter for gather data from Steam Market, use it if you want to get specific stickers
		just entered name of it
		:param _Locale language: Language settings that you can pick from Locales class
		:param _Currency currency: Currency settings that you can pick from Currencies class
		:param bool do_first_search: If true constructor will do first search
		:raises TypeError: If some type doesn't match"""

		if not (isinstance(url, str) and
		        isinstance(user_agent, str) and
		        isinstance(custom_csgo_float, str) and
		        isinstance(quantity, int) and
		        isinstance(query, str) and
		        isinstance(language, _Locale) and
		        isinstance(currency, _Currency)):
			raise TypeError

		self.__DataFetcherObject = _DataParser(url, user_agent, custom_csgo_float, quantity, query, language, currency)

		self._info: list[WeaponInfo] = self.__DataFetcherObject.get_parsed_info() if do_first_search else None

	async def iterate_once(self, interval: Union[float, int] = 0.0) -> None:
		"""Gather information in internet in coroutine and puts it in itself
		
		:param float | int interval: Interval before information will be gathered"""

		await asyncio.sleep(interval)
		self._info = self.__DataFetcherObject.get_parsed_info()

	async def loop(self, interval: Union[float, int] = 60):
		"""Stars loop that will gather information with interval
		
		:param float | int interval: Interval before information will be gathered, min value is 60 seconds
		:raises ValueError: If interval less than 30 seconds"""

		if interval < 60:
			raise ValueError

		while True:
			await self.iterate_once(interval)
			yield

	def _turn_to_dict(self) -> List[Dict[str, Any]]:
		"""Returns list with dicts instead of WeaponInfo dataclasses
		
		:return: List with dicts
		:rtype: list[dict[str, Any]]"""

		return [asdict(item) for item in self._info]

	def sorted(self, another_func_result: List[Dict[str, Any]] = None, with_stickers: bool = True,
	           with_nametag: bool = True) -> List[Dict[str, Any]]:
		"""Returns list of dicts only which contains stickers or nametag

		:param list another_func_result: Put here result from another function like filtered, to use them together
		:param bool with_stickers: Looking for lots that contains stickers
		:param bool with_nametag: Looking for lots that contains nametag
		:return: List with dicts instead of WeaponInfo dataclasses
		:rtype list[dict[str, Any]]:
		:raises TypeError: If value of arguments isn't bool"""

		if not (isinstance(with_stickers, bool) and isinstance(with_nametag, bool)):
			raise TypeError

		if not isinstance(another_func_result, list):
			info = self._turn_to_dict()
		else:
			if not another_func_result:
				return [{}]
			info = another_func_result

		sorted_info = list()

		for item in info:
			if (with_stickers and item.get('stickers')) and (with_nametag and item.get('nametag')):
				sorted_info.append(item)
			elif with_stickers and item.get('stickers'):
				sorted_info.append(item)
			elif with_nametag and item.get('nametag'):
				sorted_info.append(item)

		return sorted_info

	@staticmethod
	def _create_filter(kwargs: Dict[str, bool], all_keys: List[str]) -> Dict[str, bool]:
		"""Creates filter for filtered function from list with false bool statements

		:param dist[str, bool] kwargs: Raw filter got by **kwargs
		:param list[str] all_keys: List with all keys
		:return: Generated filter with all keys
		:rtype dist[str, bool]:"""

		statement = False

		for value in kwargs.values():
			if value:
				break
		else:
			statement = True

		for key in all_keys:
			if key not in kwargs.keys():
				kwargs.update({key: statement})
		return kwargs

	def filtered(self, another_func_result: List[Dict[str, Any]] = None, **kwargs) -> List[Dict[str, Any]]:
		"""Returns only fields that you chose

		:param list another_func_result: Put here result from another function like sorted, to use them together
		:params dict[str, bool] **kwargs: To choose the fields that you want to leave just enter their name and set True value
		:return: List of dict instead of WeaponInfo dataclasses
		:rtype list[dict[str, Any]]:
		:raises TypeError: If value in **kwargs isn't bool
		:raises ValueError: If WeaponInfo doesn't contain names of **kwargs"""

		if not isinstance(another_func_result, list):
			info = self._turn_to_dict()
		else:
			if not another_func_result:
				return [{}]
			info = another_func_result

		for key in kwargs:
			if key not in info[0]:
				raise ValueError

		for value in kwargs.values():
			if not isinstance(value, bool):
				raise TypeError

		filtered = list()
		for item in info:

			__filter = self._create_filter(kwargs, list(item.keys()))

			filtered_dict = dict()
			for key in __filter:
				if __filter[key]:
					filtered_dict.update({key: item[key]})

			filtered.append(filtered_dict)

		return filtered

	@property
	def get_as_dataclass(self) -> List[WeaponInfo]:
		"""Returns info of all reached lots in dataclass form
		
		:return: List with WeaponInfo dataclasses
		:rtype list[WeaponInfo]:"""

		if self._info is None:
			self.iterate_once()

		return self._info

	@property
	def get_as_dict(self) -> List[Dict[str, Any]]:
		"""Returns info of all reached lots in dict form
		
		:return: List with dict representations of WeaponInfo dataclass
		:rtype list[dict[str, Any]]:"""

		if self._info is None:
			self.iterate_once()

		return self._turn_to_dict()
