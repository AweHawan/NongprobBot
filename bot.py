from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# คำถามแบบทดสอบ
pretest = [
    {"q": "1. ตัวแปรสุ่มคืออะไร?", "a": "ค่าที่ขึ้นกับผลลัพธ์ของการสุ่ม"},
    {"q": "2. การแจกแจงทวินามใช้เมื่อใด?", "a": "เมื่อมีแค่ 2 ผลลัพธ์ เช่น สำเร็จ/ล้มเหลว"}
]
posttest = [
    {"q": "1. ความน่าจะเป็นรวมของทุกค่าควรเท่าไร?", "a": "1"},
    {"q": "2. ถ้าทอยลูกเต๋า 1 ครั้ง โอกาสออก 5 คือ?", "a": "1/6"}
]

# ตัวแปรสถานะ
user_data = {}

# เริ่มต้นใช้งาน
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["เริ่มแบบทดสอบก่อนเรียน", "เริ่มแบบทดสอบหลังเรียน"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("สวัสดี! เลือกแบบทดสอบที่ต้องการ 🤖", reply_markup=markup)

# เริ่มแบบทดสอบ
async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id
    mode = "pre" if "ก่อน" in text else "post"
    user_data[chat_id] = {"mode": mode, "index": 0, "score": 0}
    await send_question(update, context)

# ส่งคำถาม
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    state = user_data.get(chat_id)
    quiz = pretest if state["mode"] == "pre" else posttest
    idx = state["index"]
    if idx < len(quiz):
        await update.message.reply_text(quiz[idx]["q"])
    else:
        await update.message.reply_text(f"✅ คุณได้ {state['score']} คะแนน จาก {len(quiz)} ข้อ")
        user_data.pop(chat_id)

# ตรวจคำตอบ
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id not in user_data:
        await update.message.reply_text("พิมพ์ /start เพื่อเริ่มใหม่ครับ")
        return

    state = user_data[chat_id]
    quiz = pretest if state["mode"] == "pre" else posttest
    idx = state["index"]
    answer = update.message.text.strip()
    correct = quiz[idx]["a"]

    if answer.lower() == correct.lower():
        state["score"] += 1
        await update.message.reply_text("✅ ถูกต้อง!")
    else:
        await update.message.reply_text(f"❌ ผิดจ้า คำตอบที่ถูกคือ: {correct}")

    state["index"] += 1
    await send_question(update, context)

# เริ่มระบบ
BOT_TOKEN = "7720399028:AAFE07JsG2qR6XhzWs0ZpaQlc30apamGZpc"

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex("ก่อนเรียน|หลังเรียน"), start_quiz))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

print("✅ NongProbBot (Quiz) พร้อมทำงานแล้ว...")
app.run_polling()
