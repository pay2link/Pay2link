from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from database import get_pool


async def join_kb():

    pool = await get_pool()

    rows = await pool.fetch(
        """
        SELECT channel_name, channel_url
        FROM force_sub_channels
        ORDER BY id
        """
    )

    keyboard = []

    for row in rows:
        keyboard.append([
            InlineKeyboardButton(
                text=row["channel_name"],
                url=row["channel_url"],
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text="✅ Check",
            callback_data="check_sub",
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
