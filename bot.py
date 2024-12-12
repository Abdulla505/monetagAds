import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler

# ضع توكن البوت الخاص بك هنا
TOKEN = "8183405060:AAH4vFpWAGcpsAUx2B4_D0Du8TEBa_yayLQ"

# متغير لتخزين الرابط المؤقت
user_links = {}

# الأمر /start للترحيب بالمستخدم
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "مرحباً! أنا بوت لتحميل مقاطع الفيديو.\n"
        "أرسل لي رابط الفيديو لبدء العملية."
    )

# استقبال رابط الفيديو من المستخدم
def receive_link(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    link = update.message.text

    user_links[chat_id] = link

    # عرض أزرار الإعلانات
    keyboard = [
        [InlineKeyboardButton("مشاهدة إعلان مباشر", callback_data='direct_ad')],
        [InlineKeyboardButton("مشاهدة إعلان بمكافأة", callback_data='reward_ad')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "يرجى مشاهدة أحد الإعلانات التالية للمتابعة:",
        reply_markup=reply_markup
    )

# معالجة اختيار الإعلان
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id

    query.answer()

    if query.data == 'direct_ad':
        query.edit_message_text("تم مشاهدة الإعلان المباشر! يمكنك الآن تحميل الفيديو.")
        send_download_link(chat_id, context)
    elif query.data == 'reward_ad':
        query.edit_message_text("تم مشاهدة الإعلان بمكافأة! يمكنك الآن تحميل الفيديو.")
        send_download_link(chat_id, context)

# إرسال رابط التحميل بعد مشاهدة الإعلان
def send_download_link(chat_id, context):
    link = user_links.get(chat_id)
    if link:
        context.bot.send_message(chat_id, f"رابط التحميل الخاص بك: {link}")
        del user_links[chat_id]
    else:
        context.bot.send_message(chat_id, "لم يتم العثور على رابط. أرسل الرابط مرة أخرى.")

def main():
    # إعداد البوت
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # أوامر البوت
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_link))
    dp.add_handler(CallbackQueryHandler(button_handler))

    # بدء تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
