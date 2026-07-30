import re

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()


# =========================
# GLOBAL USER GUIDE
# =========================

@router.message()
async def notify_user(message: Message, state: FSMContext):

    # Jangan ganggu state aktif
    if await state.get_state():
        return


    # =========================
    # MEDIA DETECT
    # =========================

    if (
        message.video
        or message.photo
        or message.document
        or message.audio
        or message.animation
        or message.voice
    ):

        return await message.reply(
            "📤 <b>Upload Media</b>\n\n"
            "Untuk upload file, silakan tekan menu:\n"
            "📤 <b>Upload Media</b>\n\n"
            "Bot akan membantu membuat kode file otomatis."
        )


    # =========================
    # TEXT DETECT
    # =========================

    if not message.text:
        return


    text = message.text.strip()


    # =========================
    # CODE FILE DETECT
    # =========================

    if re.search(
        r"GGB-[A-Za-z0-9-]+",
        text,
        re.IGNORECASE
    ):

        return await message.reply(
            "📥 <b>Get Media</b>\n\n"
            "Kode file terdeteksi.\n\n"
            "Silakan buka menu:\n"
            "📥 <b>Get Media</b>\n\n"
            "Lalu kirim kode tersebut untuk mengambil file."
        )


    # =========================
    # LINK / START CODE
    # =========================

    if "start=getfile_" in text.lower():

        return await message.reply(
            "📥 <b>Get Media</b>\n\n"
            "Link file terdeteksi.\n"
            "Silakan gunakan menu 📥 <b>Get Media</b>."
        )


    # =========================
    # DEFAULT CHAT
    # =========================

    await message.reply(
        "🤖 <b>GGBOT</b>\n\n"
        "Silakan pilih menu:\n\n"
        "📤 <b>Upload Media</b>\n"
        "Upload video, foto, atau dokumen.\n\n"
        "📥 <b>Get Media</b>\n"
        "Ambil file menggunakan kode.\n\n"
        "👤 <b>Account</b>\n"
        "Kelola akun dan saldo.\n\n"
        "💎 <b>VIP</b>\n"
        "Upgrade fitur premium.\n\n"
        "ℹ️ <b>Help</b>\n"
        "Panduan penggunaan bot."
    )
