import os
from telegram import InputMediaPhoto, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# এখানে আপনার বটের টোকেনটি বসান
BOT_TOKEN = "9299542085:AAGPsNTE9GmeQ0uyf6Pmv1gjzBHp5o6dqxg"
# যে প্রাইভেট গ্রুপে ডেটা যাবে তার চ্যাট আইডি
PRIVATE_GROUP_ID = -1003839506017

# ডেটা সংগ্রহের ধাপসমূহ (Auto Pay Found সহ মোট ধাপ ১০টি করা হয়েছে)
TG_ID, INVITE_CODE, TODAY_REFER, GROUP_NO, DESIGNATION, TODAY_COMMISSION, ORDER_AMOUNT, TOTAL_ORDER, AUTO_PAY_FOUND, UPLOAD_PHOTOS = range(10)

# বটের নিচের স্থায়ী স্টার্ট বাটন (Reply Keyboard)
START_KEYBOARD = ReplyKeyboardMarkup([["🚀 Start / শুরু করুন"]], resize_keyboard=True, one_time_keyboard=True)
CANCEL_KEYBOARD = ReplyKeyboardMarkup([["❌ Cancel / বাতিল করুন"]], resize_keyboard=True)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "স্বাগতম! তথ্য জমা দেওয়া শুরু করতে নিচের **START** বাটনে ক্লিক করুন অথবা /start লিখুন।",
        reply_markup=START_KEYBOARD
    )

async def start_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Start" in text or "শুরু" in text or update.message.chat.type == "private":
        await update.message.reply_text(
            "আসুন আপনার তথ্যগুলো সংগ্রহ করি।\nপ্রথমে আপনার টেলিগ্রাম আইডি/ইউজারনেম (TG ID-@username) দিন।\n\n*(প্রক্রিয়া বাতিল করতে চাইলে নিচে Cancel বাটনে চাপুন)*",
            reply_markup=CANCEL_KEYBOARD
        )
        return TG_ID
    return ConversationHandler.END

async def get_tg_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and ("Cancel" in text or "বাতিল" in text):
        return await cancel(update, context)

    context.user_data["tg_id"] = text
    await update.message.reply_text("ধন্যবাদ। এবার আপনার ইনভাইট (Invite Code) কোডটি দিন।", reply_markup=CANCEL_KEYBOARD)
    return INVITE_CODE

async def get_invite_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and ("Cancel" in text or "বাতিল" in text):
        return await cancel(update, context)

    context.user_data["invite_code"] = text
    await update.message.reply_text("আজকে কতজনকে রেফার (Today Refer) করেছেন তার সংখ্যা লিখুন।", reply_markup=CANCEL_KEYBOARD)
    return TODAY_REFER

async def get_today_refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and ("Cancel" in text or "বাতিল" in text):
        return await cancel(update, context)

    context.user_data["today_refer"] = text
    await update.message.reply_text("আপনার গ্রুপের নম্বর (Group No) কত দিন?", reply_markup=CANCEL_KEYBOARD)
    return GROUP_NO

async def get_group_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and ("Cancel" in text or "বাতিল" in text):
        return await cancel(update, context)

    context.user_data["group_no"] = text
    await update.message.reply_text("আপনার ডেজিগনেশন (Designation) কী লিখুন।", reply_markup=CANCEL_KEYBOARD)
    return DESIGNATION

async def get_designation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and ("Cancel" in text or "বাতিল" in text):
        return await cancel(update, context)

    context.user_data["designation"] = text
    await update.message.reply_text("আজকের কমিশন (Today Commission) কত তা লিখুন।", reply_markup=CANCEL_KEYBOARD)
    return TODAY_COMMISSION

async def get_today_commission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and ("Cancel" in text or "বাতিল" in text):
        return await cancel(update, context)

    context.user_data["today_commission"] = text
    await update.message.reply_text("অর্ডারের পরিমাণ (Order Amount) কত লিখুন।", reply_markup=CANCEL_KEYBOARD)
    return ORDER_AMOUNT

async def get_order_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and ("Cancel" in text or "বাতিল" in text):
        return await cancel(update, context)

    context.user_data["order_amount"] = text
    await update.message.reply_text("মোট অর্ডার (Total Order) সংখ্যা কত লিখুন।", reply_markup=CANCEL_KEYBOARD)
    return TOTAL_ORDER

async def get_total_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and ("Cancel" in text or "বাতিল" in text):
        return await cancel(update, context)

    context.user_data["total_order"] = text
    await update.message.reply_text("অটো পে ফাউন্ড (Auto Pay Found) এর তথ্য দিন।", reply_markup=CANCEL_KEYBOARD)
    return AUTO_PAY_FOUND

async def get_auto_pay_found(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and ("Cancel" in text or "বাতিল" in text):
        return await cancel(update, context)

    context.user_data["auto_pay_found"] = text
    await update.message.reply_text(
        "ধন্যবাদ! এখন আপনার ডিভাইস থেকে যেকোনো **৩টি ছবি** (প্রমাণস্বরূপ) আপলোড করুন।\n\n*(ছবি আপলোড করার মাধ্যমেই আপনার তথ্য স্বয়ংক্রিয়ভাবে Submit হয়ে যাবে)*",
        reply_markup=CANCEL_KEYBOARD
    )
    context.user_data["photos"] = []
    return UPLOAD_PHOTOS

async def get_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        text = update.message.text
        if text and ("Cancel" in text or "বাতিল" in text):
            return await cancel(update, context)
            
        await update.message.reply_text("দয়া করে ছবি আপলোড করুন (টেক্সট নয়)। মোট ৩টি ছবি দিতে হবে।", reply_markup=CANCEL_KEYBOARD)
        return UPLOAD_PHOTOS

    photo_file = await update.message.photo[-1].get_file()
    photo_id = photo_file.file_id
    
    context.user_data["photos"].append(photo_id)
    current_count = len(context.user_data["photos"])

    if current_count < 3:
        remaining = 3 - current_count
        await update.message.reply_text(f"{current_count}টি ছবি পাওয়া গেছে। আরও {remaining}টি ছবি দিন।", reply_markup=CANCEL_KEYBOARD)
        return UPLOAD_PHOTOS
    
    # যখন ৩টি ছবি পাওয়া হয়ে যাবে (SUBMIT ধাপ সম্পন্ন)
    await update.message.reply_text("আপনার ছবি তিনটি এবং তথ্যগুলো প্রসেস ও সাবমিট করা হচ্ছে...", reply_markup=ReplyKeyboardRemove())

    user_data = context.user_data
    summary = (
        f"📥 **Today Data+Screenshot's SUBMITTED:**\n\n"
        f"👤 **TG ID:** {user_data.get('tg_id')}\n"
        f"🎟️ **Invite Code:** {user_data.get('invite_code')}\n"
        f"🫂 **Today Refer:** {user_data.get('today_refer')}\n"
        f"👥 **Group No:** {user_data.get('group_no')}\n"
        f"🪪 **Designation:** {user_data.get('designation')}\n"
        f"💰 **Today Commission:** {user_data.get('today_commission')}\n"
        f"💰 **Order Amount:** {user_data.get('order_amount')}\n"
        f"📌 **Total Order:** {user_data.get('total_order')}\n"
        f"📌 **Auto Pay Found:** {user_data.get('auto_pay_found')}"
    )

    media_group = [
        InputMediaPhoto(media=user_data["photos"][0], caption=summary, parse_mode="Markdown"),
        InputMediaPhoto(media=user_data["photos"][1]),
        InputMediaPhoto(media=user_data["photos"][2])
    ]

    try:
        await context.bot.send_media_group(chat_id=PRIVATE_GROUP_ID, media=media_group)
        await update.message.reply_text(
            "আপনার সকল তথ্য এবং ছবি সফলভাবে সাবমিট হয়ে প্রাইভেট গ্রুপে চলে গেছে! ধন্যবাদ।",
            reply_markup=START_KEYBOARD
        )
    except Exception as e:
        await update.message.reply_text(
            "দুঃখিত, গ্রুপে ডেটা পাঠাতে সমস্যা হয়েছে। দয়া করে বটকে গ্রুপের অ্যাডমিন করা আছে কিনা চেক করুন।",
            reply_markup=START_KEYBOARD
        )
        print(f"Error: {e}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "প্রক্রিয়াটি বাতিল করা হয়েছে। পুনরায় শুরু করতে নিচের START বাটনে ক্লিক করুন।",
        reply_markup=START_KEYBOARD
    )
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
            MessageHandler(filters.Regex("^(🚀 Start / শুরু করুন)$"), start_process)
        ],
        states={
            TG_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tg_id)],
            INVITE_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_invite_code)],
            TODAY_REFER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_today_refer)],
            GROUP_NO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_group_no)],
            DESIGNATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_designation)],
            TODAY_COMMISSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_today_commission)],
            ORDER_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_order_amount)],
            TOTAL_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_total_order)],
            AUTO_PAY_FOUND: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_auto_pay_found)],
            UPLOAD_PHOTOS: [MessageHandler(filters.PHOTO | filters.TEXT, get_photos)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(filters.Regex("^(❌ Cancel / বাতিল করুন)$"), cancel)
        ],
    )

    app.add_handler(conv_handler)
    
    print("Bot is running with Auto Pay Found & 3 photos support...")
    app.run_polling()

if __name__ == "__main__":
    main()
