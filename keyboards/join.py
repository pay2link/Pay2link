from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from database import get_pool


async def join_kb(lang: str = "en"):

    if lang.startswith("id"):
        check_text = "✅ Cek Bergabung"
    else:
        check_text = "✅ Check Membership"

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
            text=check_text,
            callback_data="check_sub",
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
