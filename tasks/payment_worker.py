import asyncio
import logging

from database import fetch, fetchrow, execute
from utils.bayargg import BayarGG
from bot import bot


logger = logging.getLogger(__name__)


CHANNEL_PAYMENT = -1003894841696

CHECK_INTERVAL = 10


SUCCESS_STATUS = [
    "success",
    "paid",
    "settlement",
    "completed",
    "berhasil"
]


async def payment_worker():

    logger.info(
        "💳 Payment worker running..."
    )


    while True:

        try:

            payments = await fetch(
                """
                SELECT
                    id,
                    user_id,
                    file_code,
                    owner_id,
                    paid_price,
                    invoice_id
                FROM file_purchases
                WHERE status='pending'
                ORDER BY id ASC
                LIMIT 50
                """
            )


            for pay in payments:

                invoice_id = pay["invoice_id"]


                try:

                    # =========================
                    # CEK BAYARGG
                    # =========================

                    result = await BayarGG.check_payment(
                        invoice_id
                    )


                    logger.info(
                        "CHECK %s => %s",
                        invoice_id,
                        result
                    )


                    if not result:
                        continue



                    status = str(
                        result.get("status", "")
                    ).lower()



                    if status not in SUCCESS_STATUS:

                        continue



                    # =========================
                    # LOCK STATUS
                    # =========================

                    current = await fetchrow(
                        """
                        SELECT status
                        FROM file_purchases
                        WHERE invoice_id=$1
                        """,
                        invoice_id
                    )


                    if not current:
                        continue


                    if current["status"] == "paid":

                        logger.info(
                            "SKIP ALREADY PAID %s",
                            invoice_id
                        )

                        continue



                    # =========================
                    # UPDATE PAID
                    # =========================

                    await execute(
                        """
                        UPDATE file_purchases
                        SET
                            status='paid'
                        WHERE invoice_id=$1
                        """,
                        invoice_id
                    )


                    logger.info(
                        "✅ PAYMENT SUCCESS %s",
                        invoice_id
                    )



                    # =========================
                    # POST CHANNEL
                    # =========================

                    try:

                        await bot.send_message(
                            chat_id=CHANNEL_PAYMENT,
                            text=(
                                "💰 <b>PEMBAYARAN BERHASIL</b>\n\n"
                                f"👤 User ID : "
                                f"<code>{pay['user_id']}</code>\n"
                                f"📁 File Code : "
                                f"<code>{pay['file_code']}</code>\n"
                                f"💵 Harga : "
                                f"Rp {pay['paid_price']:,}\n"
                                f"🧾 Invoice : "
                                f"<code>{invoice_id}</code>\n\n"
                                "✅ File berhasil dibeli."
                            ).replace(",", "."),
                            parse_mode="HTML"
                        )


                        logger.info(
                            "CHANNEL POST OK %s",
                            invoice_id
                        )


                    except Exception:

                        logger.exception(
                            "CHANNEL POST ERROR %s",
                            invoice_id
                        )



                    # =========================
                    # TODO KIRIM FILE
                    # =========================

                    # nanti sambungkan handler
                    # send_file(pay["user_id"], pay["file_code"])



                except Exception:

                    logger.exception(
                        "PROCESS PAYMENT ERROR %s",
                        invoice_id
                    )



        except Exception:

            logger.exception(
                "PAYMENT WORKER LOOP ERROR"
            )


        await asyncio.sleep(
            CHECK_INTERVAL
        )
