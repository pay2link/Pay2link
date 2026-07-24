from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def join_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢Channel Code",
                    url="https://t.me/+-su4qQpS2n04OTFl"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢Channel Update",
                    url="https://t.me/+e3qQQNePX3k1ZjFl"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ CHECK",
                    callback_data="check_sub"
                )
            ]
        ]
    )
