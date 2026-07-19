from enum import StrEnum

class LocaleFlags(StrEnum):
    ENGLISH = "🇬🇧"
    RUSSIAN = "🇷🇺"
    UKRAINIAN = "🇺🇦"

class Locale(StrEnum):
    ENGLISH = "en"
    RUSSIAN = "ru"
    UKRAINIAN = "uk"