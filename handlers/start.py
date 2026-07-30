import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.force_sub import check_force_sub
from utils.lang import get_text
from keyboards.menu import home_kb
from keyboards.join import join_kb
from keyboards.language import language_kb
from database import get_pool

router = Router()


# =========================
# START
# =========================

@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):

    await state.clear()

    user_id = message.from_user.id
    username = message.from_user.username or "unknown"

    try:
        pool = await get_pool()

        await pool.execute(
            """
            INSERT INTO users
            (
                telegram_id,
                username,
                chat_id,
                balance
            )
            VALUES
            ($1,$2,$3,0)
            ON CONFLICT (telegram_id)
            DO UPDATE SET
                username = EXCLUDED.username,
                chat_id = EXCLUDED.chat_id
            """,
            user_id,
            username,
            message.chat.id
        )

        lang = await pool.fetchval(
            """
            SELECT language
            FROM users
            WHERE telegram_id=$1
            """,
            user_id
        )

        if not lang:
            return await message.answer(
                "🌐 <b>Select Language / Pilih Bahasa</b>\n\n"
                "🇮🇩 Silakan pilih bahasa.\n"
                "🇺🇸 Please choose your language.",
                parse_mode="HTML",
                reply_markup=language_kb()
            )

        loading = await message.answer(
            get_text(lang, "loading"),
            parse_mode="HTML"
        )

        await process_start(
            message,
            loading,
            user_id,
            username,
            lang
        )

    except Exception:
        logging.exception("START ERROR")

        await message.answer(
            "❌ <b>System Error</b>",
            parse_mode="HTML"
        )


# =========================
# PROCESS START
# =========================

async def process_start(message, loading, user_id, username, lang):

    try:
        sub = await check_force_sub(
            message.bot,
            user_id
        )

    except Exception:
        sub = True

    if not sub:
        return await loading.edit_text(
            get_text(lang, "join_required"),
            parse_mode="HTML",
            reply_markup=join_kb()
        )

    pool = await get_pool()

    user = await pool.fetchrow(
        """
        SELECT username, balance
        FROM users
        WHERE telegram_id=$1
        """,
        user_id
    )

    await render_home_fast(
        message.bot,
        loading,
        user_id,
        user["username"] or username,
        user["balance"] or 0,
        lang
    )


# =========================
# HOME UI
# =========================

async def render_home_fast(bot, message, user_id, username, balance, lang):

    balance = f"{int(balance):,}".replace(",", ".")

    text = (
        "🤖 <b>𝗚𝗚𝗕𝗢𝗧</b>\n"
        "<i>Smart File Sharing Platform</i>\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🆔 <b>User ID</b>\n"
        f"<code>{user_id}</code>\n\n"
        f"👤 <b>Username</b>\n"
        f"@{username}\n\n"
        f"💰 <b>Balance</b>\n"
        f"<code>Rp {balance}</code>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"{get_text(lang, 'welcome')}"
    )

    try:
        await message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=home_kb()
        )

    except Exception:
        await bot.send_message(
            user_id,
            text,
            parse_mode="HTML",
            reply_markup=home_kb()
        )


# =========================
# CALLBACK HOME
# =========================

@router.callback_query(F.data == "home")
async def back_home(call: CallbackQuery, state: FSMContext):

    await call.answer()
    await state.clear()

    user_id = call.from_user.id

    pool = await get_pool()

    lang = await pool.fetchval(
        """
        SELECT language
        FROM users
        WHERE telegram_id=$1
        """,
        user_id
    ) or "id"

    try:
        ok = await check_force_sub(
            call.bot,
            user_id
        )

    except Exception:
        ok = True

    if not ok:
        return await call.message.answer(
            get_text(lang, "join_required"),
            parse_mode="HTML",
            reply_markup=join_kb()
        )

    user = await pool.fetchrow(
        """
        SELECT username, balance
        FROM users
        WHERE telegram_id=$1
        """,
        user_id
    )

    await render_home_fast(
        call.bot,
        call.message,
        user_id,
        user["username"] or "unknown",
        user["balance"] or 0,
        lang
    )
