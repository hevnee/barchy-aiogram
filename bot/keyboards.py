from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data="uk"),
        ],
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data="en"),
            InlineKeyboardButton(text="🇵🇱 Polski", callback_data="pl"),
        ]
    ]
)

def show_original_keyboard(lang_dict: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"📄 {lang_dict['show_original_lang']}", callback_data="show_original"),
            ]
        ]
    )

def show_translation_keyboard(lang_dict: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"📄 {lang_dict['show_translation_lang']}", callback_data="show_translation")
            ]
        ]
    )

#history show_original
def history_show_original(current_page: int, total_pages: int, date: str, lang_dict: dict, lang: str):
    return create_history_keyboard(
        current_page, total_pages, date, lang_dict, lang,
        [InlineKeyboardButton(text=f"{lang_dict[lang]['show_original_lang']} 📄", callback_data="show_original_h")]
    )

#history show_translation
def history_show_translation(current_page: int, total_pages: int, date: str, lang_dict: dict, lang: str):
    return create_history_keyboard(
        current_page, total_pages, date, lang_dict, lang,
        [InlineKeyboardButton(text=f"{lang_dict[lang]['show_translation_lang']} 📄", callback_data="show_translation_h")]
    )

#history keyboard
def create_history_keyboard(current_page: int, total_pages: int, date: str, lang_dict: dict, lang: str, extra_buttons: list):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"⬅️ {lang_dict[lang]['prev']}", callback_data="prev_h"),
            InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="reset_h"),
            InlineKeyboardButton(text=f"{lang_dict[lang]['next']} ➡️", callback_data="next_h"),
        ],
        [
            InlineKeyboardButton(text=f"⌚️ {date}", callback_data="date_h"),
            *extra_buttons
        ],
        [
            InlineKeyboardButton(text=f"🗑 {lang_dict[lang]['del_this']}", callback_data="delete_this_request_h"),
            InlineKeyboardButton(text=f"{lang_dict[lang]['del_all']} 🗑", callback_data="delete_all_h"),
        ]
    ])

def confirmation_keyboard(yes: str, lang_dict: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"✅ {lang_dict['yes']}", callback_data=yes),
                InlineKeyboardButton(text=f"{lang_dict['no']} ❌", callback_data="no_c")
            ]
        ]
    )

def update_history_keyboard(lang_dict: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🔄 {lang_dict['update_h']}", callback_data="update_h")
            ]
        ]
    )

def giveaway_keyboard(lang_dict: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=lang_dict["giveaway_participate"], callback_data="giveaway_participate")
            ]
        ]
    )

def change_style_keyboard(lang_dict: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=lang_dict["style_normal_button"], callback_data="style_normal"),
                InlineKeyboardButton(text=lang_dict["style_wise_button"], callback_data="style_wise")
            ],
            [
                InlineKeyboardButton(text=lang_dict["style_sarcastic_button"], callback_data="style_sarcastic"),
                InlineKeyboardButton(text=lang_dict["style_bastard_button"], callback_data="style_bastard")
            ]
        ]
    )