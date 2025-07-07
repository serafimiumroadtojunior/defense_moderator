from aiogram.filters.callback_data import CallbackData


class ModerationCallback(CallbackData, prefix='moderation'):
    action: str
    user_id: int


class LanguageCallback(CallbackData, prefix='language'):
    language: str