from dataclasses import dataclass


@dataclass
class _Currency:
	"""Currency dataclass that contains currency preferences"""
	currency_api: str
	currency_tag: str


@dataclass
class _Locale:
	"""Locale dataclass that contains language preferences"""
	language: str


class Locales:
	"""Locales class that contains language preferences"""
	US = _Locale('english')
	UA = _Locale('ukrainian')
	RU = _Locale('russian')


class Currencies:
	"""Currencies class that contains currency preferences"""
	USD = _Currency('1', '$')
	UAH = _Currency('18', '₴')
	RUB = _Currency('5', '₽')
