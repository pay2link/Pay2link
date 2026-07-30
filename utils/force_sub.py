import logging

from aiogram import Bot
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
)

from database import get_pool


# =========================
# CHECK FORCE SUBSCRIBE
# =========================
async def check_force_sub(bot: Bot, user_id: int) -> bool:
    """
    Return:
        True  -> User sudah join semua channel.
        False -> User belum join salah satu channel.
    """

    pool = await get_pool()

    channels = await pool.fetch(
        """
        SELECT channel_id
        FROM force_sub_channels
        ORDER BY id
        """
    )

    # Jika belum ada channel, izinkan semua user.
    if not channels:
        return True

    for row in channels:
        channel_id = row["channel_id"]

        try:
            member = await bot.get_chat_member(
                chat_id=channel_id,
                user_id=user_id,
            )

            if member.status not in (
                "member",
                "administrator",
                "creator",
            ):
                return False

        except (TelegramBadRequest, TelegramForbiddenError) as e:
            logging.error(
                "ForceSub Error | Channel=%s User=%s Error=%s",
                channel_id,
                user_id,
                e,
            )
            return True

        except Exception:
            logging.exception(
                "ForceSub Unknown Error | Channel=%s User=%s",
                channel_id,
                user_id,
            )
            return True

    return True
