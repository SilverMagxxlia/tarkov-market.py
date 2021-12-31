from enum import StrEnum


class Rarity(StrEnum):
    rare: str = 'Rare'
    common: str = 'Common'
    not_exist: str = 'Not_exist'


class LangType(StrEnum):
    ENGLISH: str = 'en'
    RUSSIAN: str = 'ru'
    DEUTSCH: str = 'de'
    FRENCH: str = 'fr'
    SPANISH: str = 'es'
    ESPANOL: str = SPANISH
    CHINESE: str = 'cn'
    CZECH: str = 'cz'
    HUNGARIAN: str = 'hu'
    TURKISH: str = 'tu'
