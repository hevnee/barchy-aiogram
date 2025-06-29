from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#language keyboard
language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
        InlineKeyboardButton(text="🇺🇦 Українська", callback_data="uk")
    ],
    [
        InlineKeyboardButton(text="🇬🇧 English", callback_data="en"),
        InlineKeyboardButton(text="🇵🇱 Polski", callback_data="pl")
    ],
    [
        InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="de"),
        InlineKeyboardButton(text="🇫🇷 Français", callback_data="fr")
    ],
    [
        InlineKeyboardButton(text="🇪🇸 Español", callback_data="es"),
        InlineKeyboardButton(text="🇹🇷 Türkiye", callback_data="tr")
    ]
])

#show translation keyboard
def STkeyboard(SELECTED_LANGUAGE: dict, lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"📄 {SELECTED_LANGUAGE[lang]['show_translation_lang']}", callback_data="show_translation")
        ]
    ])

#show original keyboard
def SOkeyboard(SELECTED_LANGUAGE: dict, lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"📄 {SELECTED_LANGUAGE[lang]['show_original_lang']}", callback_data="show_original")
        ]
    ])

#history show_original
def Hkeyboard(current_page: int, total_pages: int, date: str, SELECTED_LANGUAGE: dict, lang: str):
    return create_Hkeyboard(
        current_page, total_pages, date, SELECTED_LANGUAGE, lang,
        [InlineKeyboardButton(text=f"{SELECTED_LANGUAGE[lang]['show_original_lang']} 📄", callback_data="show_original_h")]
    )

#history show_translation
def Hkeyboard_translation(current_page: int, total_pages: int, date: str, SELECTED_LANGUAGE: dict, lang: str):
    return create_Hkeyboard(
        current_page, total_pages, date, SELECTED_LANGUAGE, lang,
        [InlineKeyboardButton(text=f"{SELECTED_LANGUAGE[lang]['show_translation_lang']} 📄", callback_data="show_translation_h")]
    )

#history keyboard
def create_Hkeyboard(current_page: int, total_pages: int, date: str, SELECTED_LANGUAGE: dict, lang: str, extra_buttons: list):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"⬅️ {SELECTED_LANGUAGE[lang]['prev']}", callback_data="prev_h"),
            InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="reset_h"),
            InlineKeyboardButton(text=f"{SELECTED_LANGUAGE[lang]['next']} ➡️", callback_data="next_h"),
        ],
        [
            InlineKeyboardButton(text=f"⌚️ {date}", callback_data="date_h"),
            *extra_buttons
        ],
        [
            InlineKeyboardButton(text=f"🗑 {SELECTED_LANGUAGE[lang]['del_this']}", callback_data="delete_this_request_h"),
            InlineKeyboardButton(text=f"{SELECTED_LANGUAGE[lang]['del_all']} 🗑", callback_data="delete_all_h"),
        ]
    ])

#confirmation keyboard
def Ckeyboard(yes: str, SELECTED_LANGUAGE: dict, lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"✅ {SELECTED_LANGUAGE[lang]['yes']}", callback_data=yes),
            InlineKeyboardButton(text=f"{SELECTED_LANGUAGE[lang]['no']} ❌", callback_data="no_c")
        ]
    ])

#update_history keyboard
def UHkeyboard(SELECTED_LANGUAGE: dict, lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🔄 {SELECTED_LANGUAGE[lang]['update_h']}", callback_data="update_h")]])
