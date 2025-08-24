import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from strategy import check_signal
from risk import can_open_trade, TRADE_SIZE
import delta_client

# Store trades in memory
open_trades = []


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running. Ready for signals!")


# /signal open high low close
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = list(map(float, context.args))
        if len(args) != 4:
            await update.message.reply_text("Usage: /signal open high low close")
            return

        open_, high, low, close = args
        pivots = list(map(float, os.getenv("PIVOTS", "90,95,100").split(",")))

        side = check_signal(open_, high, low, close, pivots)

        if not side:
            await update.message.reply_text("No trade signal.")
            return

        if not can_open_trade(open_trades):
            await update.message.reply_text("⚠️ Max trades open. Skipping.")
            return

        # Calculate SL (25% of pivot gap)
        gap = abs(pivots[1] - pivots[0])
        if side == "LONG":
            entry = pivots[1]
            sl = entry - 0.25 * gap
        else:
            entry = pivots[1]
            sl = entry + 0.25 * gap

        # Place dummy order
        delta_client.place_order(side, TRADE_SIZE, price=entry, stop_loss=sl)
        open_trades.append({"side": side, "entry": entry, "sl": sl})

        await update.message.reply_text(
            f"📈 {side} trade entered at {entry}, SL={sl}"
        )

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


# /flatten
async def flatten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    delta_client.cancel_all()
    open_trades.clear()
    await update.message.reply_text("🛑 All trades closed.")


def main():
    token = os.getenv("TELEGRAM_TOKEN")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("flatten", flatten))

    print("🤖 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
