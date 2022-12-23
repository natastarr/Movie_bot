from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Rating content keyboard
_inline_btn_rating_yes = InlineKeyboardButton('Yes', callback_data='rating_true')
_inline_btn_rating_no = InlineKeyboardButton('No', callback_data='rating_false')
inline_rating_kb = InlineKeyboardMarkup().row(_inline_btn_rating_yes, _inline_btn_rating_no)


# Settings keyboard
_inline_btn_settings_rating = InlineKeyboardButton('Rating content', callback_data='settings_rating')
inline_settings_kb = InlineKeyboardMarkup()
inline_settings_kb.add(_inline_btn_settings_rating)
