import asyncio
import logging

from database import fetch, fetchrow, execute
from utils.bayargg import BayarGG
from bot import bot


logger = logging.getLogger(__name__)


CHANNEL_PAYMENT = -1003894841696

CHECK_INTERVAL = 10


async def payment_worker():

    logger.info("💳 Payment worker running...")


    while True:

        try:

            # =========================
            # AMBIL PAYMENT PENDING
            # =========================

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


            if not payments:

                await asyncio.sleep(
                    CHECK_INTERVAL
                )

                continue



            for pay in payments:


                invoice_id = pay["invoice_id"]


                try:

                    # =========================
                    # CEK STATUS BAYARGG
                    # =========================

                    result = await BayarGG.check_payment(
                        invoice_id
                    )


                    logger.info(
                        "CHECK PAYMENT %s | %s",
                        invoice_id,
                        result
                    )


                    if not result:

                        continue



                    status = (
                        result.get("status")
                        or ""
                    ).lower()



                    if status not in [
                        "success",
                        "paid",
                        "settlement"
                    ]:

                        continue



                    # =========================
                    # CEK ULANG AGAR TIDAK DOUBLE
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
                        "PAYMENT PAID %s",
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
                                f"📁 File : "
                                f"<code>{pay['file_code']}</code>\n"
                                f"💵 Harga : "
                                f"Rp {pay['paid_price']:,}\n"
                                f"🧾 Invoice : "
                                f"<code>{invoice_id}</code>\n\n"
                                "✅ Pembelian berhasil."
                            ).replace(",", "."),
                            parse_mode="HTML"
                        )


                    except Exception:

                        logger.exception(
                            "CHANNEL POST FAILED"
                        )



                    # =========================
                    # LANJUT KIRIM FILE
                    # =========================

                    # TODO:
                    # panggil fungsi kirim file
                    # yang sudah kamu punya disini



                except Exception:

                    logger.exception(
                        "PROCESS PAYMENT ERROR %s",
                        invoice_id
                    )



        except Exception:

            logger.exception(
                "PAYMENT WORKER ERROR"
            )



        await asyncio.sleep(
            CHECK_INTERVAL
        )
