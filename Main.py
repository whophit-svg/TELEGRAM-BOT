import logging
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuration Details (Directly configured)
TOKEN = "8330012138:AAEGJ7EPzzinYTBFw8GiXuQklsPrTZAGEeM"
TARGET_CHANNEL = "@ZENITH_KINGDOM"

# All Custom Premium Emojis (HTML Format)
EMOJI_1 = '<tg-emoji emoji-id="6267118537752450044">✨</tg-emoji>'
EMOJI_2 = '<tg-emoji emoji-id="6267225207560214192">🌟</tg-emoji>'
EMOJI_3 = '<tg-emoji emoji-id="6266969287638913443">🎉</tg-emoji>'
EMOJI_4 = '<tg-emoji emoji-id="5974375619851460040">⚡</tg-emoji>'
EMOJI_5 = '<tg-emoji emoji-id="5260632384029621402">🚀</tg-emoji>'
EMOJI_6 = '<tg-emoji emoji-id="5258089552936994416">💎</tg-emoji>'
EMOJI_7 = '<tg-emoji emoji-id="5883964170268840032">🔥</tg-emoji>'
EMOJI_8 = '<tg-emoji emoji-id="6267291337171670780">👑</tg-emoji>'
EMOJI_9 = '<tg-emoji emoji-id="6136479887604586527">💫</tg-emoji>'

# Error Premium Emoji
EMOJI_ERROR = '<tg-emoji emoji-id="6267000941547885720">❌</tg-emoji>'

# Short & Small-caps Stylized Text for Group Response
SHORT_VOUCH_TEXT = "ᴠᴏᴜᴄʜ ꜱᴜʙᴍɪᴛᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ"

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    message = update.message

    if not chat or not user:
        return

    if chat.type == "private":
        await update.message.reply_text(
            f"{EMOJI_ERROR} <b>ᴘʟᴇᴀꜱᴇ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴꜱɪᴅᴇ ᴀ ɢʀᴏᴜᴘ!</b> {EMOJI_ERROR}",
            parse_mode="HTML"
        )
        return

    # Safe user name handling and HTML escaping
    user_name = html.escape(user.full_name)
    profile_link = f"<a href='tg://user?id={user.id}'>{user_name}</a>"
    chat_title = html.escape(chat.title) if chat.title else "Group"

    # Extract feedback text safely from args or caption
    feedback_text = " ".join(context.args) if context.args else ""

    if not feedback_text and message.caption:
        caption_words = message.caption.split()
        if caption_words and caption_words[0].startswith('/fb'):
            feedback_text = " ".join(caption_words[1:])

    # Escape feedback text to prevent HTML formatting crash bugs
    safe_feedback_text = html.escape(feedback_text) if feedback_text else ""

    # Formatted Channel Post
    formatted_details = (
        f"{EMOJI_1} {EMOJI_6} <b>ɴᴇᴡ ᴠᴏᴜᴄʜ ʀᴇᴄᴇɪᴠᴇᴅ</b> {EMOJI_2} {EMOJI_7}\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>ᴜꜱᴇʀ:</b> {profile_link} {EMOJI_4} {EMOJI_8}\n"
        f"🆔 <b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{user.id}</code> {EMOJI_5}\n"
        f"💬 <b>ɢʀᴏᴜᴘ:</b> <b>{chat_title}</b> {EMOJI_3} {EMOJI_9}\n"
    )

    if safe_feedback_text:
        formatted_details += f"\n📝 <b>ᴠᴏᴜᴄʜ:</b>\n<b>{safe_feedback_text}</b> {EMOJI_1} {EMOJI_6}\n"

    formatted_details += "━━━━━━━━━━━━━━━━━━━━━"

    # Inline Keyboard Button linking to @ZENITH_OG
    keyboard = [
        [InlineKeyboardButton("👑 OWNER", url="https://t.me/ZENITH_OG")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if message.reply_to_message:
            replied_msg = message.reply_to_message
            if replied_msg.photo:
                photo_file_id = replied_msg.photo[-1].file_id
                await context.bot.send_photo(
                    chat_id=TARGET_CHANNEL,
                    photo=photo_file_id,
                    caption=formatted_details,
                    parse_mode="HTML",
                    reply_markup=reply_markup
                )
            elif replied_msg.video:
                await context.bot.send_video(
                    chat_id=TARGET_CHANNEL,
                    video=replied_msg.video.file_id,
                    caption=formatted_details,
                    parse_mode="HTML",
                    reply_markup=reply_markup
                )
            else:
                await context.bot.send_message(
                    chat_id=TARGET_CHANNEL,
                    text=formatted_details,
                    parse_mode="HTML",
                    reply_markup=reply_markup
                )

        elif message.photo:
            photo_file_id = message.photo[-1].file_id
            await context.bot.send_photo(
                chat_id=TARGET_CHANNEL,
                photo=photo_file_id,
                caption=formatted_details,
                parse_mode="HTML",
                reply_markup=reply_markup
            )

        elif message.video:
            await context.bot.send_video(
                chat_id=TARGET_CHANNEL,
                video=message.video.file_id,
                caption=formatted_details,
                parse_mode="HTML",
                reply_markup=reply_markup
            )

        else:
            await context.bot.send_message(
                chat_id=TARGET_CHANNEL,
                text=formatted_details,
                parse_mode="HTML",
                reply_markup=reply_markup
            )

        # Short & Clean Response in Group with Premium Emojis
        await update.message.reply_text(
            f"{EMOJI_3} {EMOJI_8} <b>{SHORT_VOUCH_TEXT}</b> {EMOJI_1} {EMOJI_5}",
            parse_mode="HTML"
        )

    except Exception as e:
        logging.error(f"Error sending feedback: {e}")
        await update.message.reply_text(
            f"{EMOJI_ERROR} <b>ᴇʀʀᴏʀ:</b> <code>{html.escape(str(e))}</code> {EMOJI_ERROR}",
            parse_mode="HTML"
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("fb", feedback))

    print("🚀 Premium Feedback Bot is running successfully...")
    app.run_polling()
  
