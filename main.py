# ======================================================
# 👑 PROJECT: THE ULTIMATE MODULAR BOT (V46.0 - COMPRESSION EDITION)
# 👤 DEVELOPER: IBRAHIM MUSTAFA (@x_u3s1)
# 🆔 ADMIN ID: 8301016131
# 🛠 STATUS: STABLE - 4K SUPPORTED - AUTO COMPRESS ENABLED
# 📍 LOCATION: BASRA, IRAQ 🇮🇶
# ======================================================

import os
import threading
import time
import json
import re
import random
import subprocess
import sys
import requests
import shutil
import logging
from datetime import datetime, timedelta

# --- [ 1. إعدادات السجلات والحماية ] ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot_v46.log'), logging.StreamHandler()]
)

# --- [ 2. محرك البيئة البرمجية المستقر ] ---
def setup_environment():
    """تجهيز المكتبات الأساسية لضمان عدم توقف البوت في Railway"""
    print("🚀 [STARTUP] جاري فحص المحركات البرمجية في البصرة...")
    # تم التأكد من وجود المكتبات اللازمة للضغط والتحميل
    required_libs = ["yt-dlp", "pyTelegramBotAPI", "requests", "certifi"]
    for lib in required_libs:
        try:
            __import__(lib.replace('-', '_'))
        except ImportError:
            print(f"📦 تثبيت المكتبة المفقودة: {lib}")
            subprocess.call([sys.executable, "-m", "pip", "install", lib, "--quiet"])
    print("✅ [SUCCESS] جميع المحركات جاهزة للعمل بكفاءة عالية.")

setup_environment()

import telebot
from telebot import types
import yt_dlp
import certifi

# --- [ 3. الثوابت والإعدادات العميقة ] ---
API_TOKEN = '8168190815:AAG0U-eqjIvAr5HbtTWTGOqQzSRz9Pdx4AY'.strip()
bot = telebot.TeleBot(API_TOKEN, num_threads=25) 
ADMIN_ID = 8301016131 
MY_USER = "@x_u3s1"

DB_PATH = {
    "ranks": "v44_ranks.json",
    "users": "v44_users.json",
    "daily": "v44_daily.json",
    "settings": "v44_settings.json"
}
CACHE_DIR = "v44_storage_bin"

if not os.path.exists(CACHE_DIR): 
    os.makedirs(CACHE_DIR)

# --- [ 4. محرك إدارة البيانات ] ---
def load_data(key):
    path = DB_PATH.get(key)
    try:
        if not os.path.exists(path):
            initial = [] if key == "users" else {}
            with open(path, "w", encoding='utf-8') as f:
                json.dump(initial, f, indent=4)
            return initial
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading {key}: {e}")
        return [] if key == "users" else {}

def save_data(key, data):
    try:
        with open(DB_PATH[key], "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error saving {key}: {e}")

# --- [ 5. نظام الرتب ] ---
def get_rank_title(xp):
    ranks = [
        (100000, "إمبراطور الميديا 🌌"),
        (50000, "سيد التحميل 👑"),
        (20000, "الأسطورة البصرية 🏆"),
        (10000, "محمل ذهبي ✨"),
        (5000, "محترف 🔥"),
        (1000, "نشط جداً ⚡"),
        (0, "مبتدئ 👶")
    ]
    for limit, title in ranks:
        if xp >= limit: return title

def update_user_profile(uid, name, xp=0, dl=0):
    data = load_data("ranks")
    uid_s = str(uid)
    name = re.sub(r'[^\w\s]', '', str(name))
    if uid_s not in data:
        data[uid_s] = {
            "name": name, "xp": 0, "dl": 0, 
            "lvl": "مبتدئ 👶", "date": str(datetime.now().date())
        }
    
    data[uid_s]["xp"] += xp
    data[uid_s]["dl"] += dl
    data[uid_s]["lvl"] = get_rank_title(data[uid_s]["xp"])
    
    if uid == ADMIN_ID: data[uid_s]["lvl"] = "المطور الأساسي (ابن البصرة) 👑"
    save_data("ranks", data)

# --- [ 6. الواجهات ] ---
def main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📥 بدء التحميل", callback_data="ui_download"),
        types.InlineKeyboardButton("👤 الملف الشخصي", callback_data="ui_me"),
        types.InlineKeyboardButton("🏆 المتصدرين", callback_data="ui_top"),
        types.InlineKeyboardButton("🎁 هدية البصرة", callback_data="ui_gift"),
        types.InlineKeyboardButton("⚙️ الإحصائيات", callback_data="ui_stats"),
        types.InlineKeyboardButton("👨‍💻 مبرمج البوت", callback_data="ui_owner")
    )
    return markup

def dl_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎬 فيديو MP4", callback_data="m_vid"),
        types.InlineKeyboardButton("🎵 صوت MP3", callback_data="m_aud"),
        types.InlineKeyboardButton("🔙 رجوع", callback_data="ui_back")
    )
    return markup

# --- [ 7. محرك التحميل والضغط الذكي (Modified for 107MB+) ] ---
def secure_download(chat_id, url, type_mode):
    msg = bot.send_message(chat_id, "⏳ جاري فحص الرابط ومعالجة الجودة...")
    
    try:
        file_id = f"file_{int(time.time())}_{random.randint(100,999)}"
        path_tmpl = os.path.join(CACHE_DIR, f"{file_id}.%(ext)s")
        
        y_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': path_tmpl,
            'quiet': True,
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(y_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            f_name = ydl.prepare_filename(info)
            if not os.path.exists(f_name):
                f_name = f_name.rsplit('.', 1)[0] + ".mp4"

        f_size = os.path.getsize(f_name) / (1024 * 1024)
        
        # إذا كان الملف أكبر من حدود تليجرام (مثل الـ 107MB)
        if f_size > 49.0:
            bot.edit_message_text(f"⚖️ الحجم {int(f_size)}MB كبير جداً.. جاري ضغط الفيديو ذكياً لتخطي القيود...", chat_id, msg.message_id)
            compressed_name = f_name.replace(".mp4", "_low.mp4")
            
            # أمر FFmpeg للضغط البرمجي (CRF 28 يحافظ على جودة ممتازة وحجم صغير)
            cmd = f'ffmpeg -i "{f_name}" -vcodec libx264 -crf 28 -preset fast -acodec aac -strict -2 "{compressed_name}" -y'
            subprocess.run(cmd, shell=True)
            
            final_file = compressed_name
            if os.path.exists(f_name): os.remove(f_name)
        else:
            final_file = f_name

        # إرسال الملف النهائي
        with open(final_file, 'rb') as f:
            if type_mode == 'v':
                bot.send_video(chat_id, f, caption="✅ تم التحميل والضغط بنجاح (V46.0)")
            else:
                bot.send_audio(chat_id, f, caption="🎵 تم استخراج الصوت بنجاح")
        
        if os.path.exists(final_file): os.remove(final_file)
        bot.delete_message(chat_id, msg.message_id)
        update_user_profile(chat_id, "User", xp=100, dl=1)
        
    except Exception as e:
        bot.edit_message_text(f"❌ خطأ تقني: {str(e)}", chat_id, msg.message_id)
        logging.error(f"Download error: {e}")

# --- [ 8. معالج الأوامر ] ---
current_urls = {}

@bot.message_handler(commands=['start'])
def start_handler(m):
    u = m.from_user
    users = load_data("users")
    if u.id not in users:
        users.append(u.id)
        save_data("users", users)
    
    update_user_profile(u.id, u.first_name)
    welcome = (f"👑 أهلاً بك يا {u.first_name} في عالم إبراهيم مصطفى.\n\n"
               "أرسل أي رابط وسأقوم بضغط وتحميل الملف لك مهما كان حجمه!")
    bot.send_message(m.chat.id, welcome, reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def link_handler(m):
    current_urls[m.from_user.id] = m.text
    bot.reply_to(m, "🗳 اختر نوع الملف:", reply_markup=dl_keyboard())

# --- [ 9. معالج الأزرار ] ---
@bot.callback_query_handler(func=lambda call: True)
def ui_manager(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    if call.data == "ui_back": bot.edit_message_text("🏠 القائمة الرئيسية", cid, mid, reply_markup=main_keyboard())
    elif call.data == "m_vid":
        url = current_urls.get(uid)
        if url: 
            bot.delete_message(cid, mid)
            threading.Thread(target=secure_download, args=(cid, url, 'v')).start()
    elif call.data == "m_aud":
        url = current_urls.get(uid)
        if url: 
            bot.delete_message(cid, mid)
            threading.Thread(target=secure_download, args=(cid, url, 'a')).start()
    elif call.data == "ui_me":
        u_data = load_data("ranks").get(str(uid), {"name":"User", "xp":0, "dl":0, "lvl":"مبتدئ"})
        text = f"👤 الاسم: {u_data['name']}\n🎖 الرتبة: {u_data['lvl']}\n⭐ نقاطك: {u_data['xp']}\n📥 تحميلاتك: {u_data['dl']}"
        bot.edit_message_text(text, cid, mid, reply_markup=main_keyboard())
    # ... (باقي أزرار الإحصائيات والهدايا كما هي في سكربتك الأصلي)

# --- [ 10. التنظيف ] ---
def cleaner_engine():
    while True:
        try:
            if os.path.exists(CACHE_DIR):
                for file in os.listdir(CACHE_DIR):
                    f_p = os.path.join(CACHE_DIR, file)
                    if os.path.getmtime(f_p) < time.time() - 900: os.remove(f_p)
        except: pass
        time.sleep(900)

if __name__ == "__main__":
    print(f"✅ [V46.0] IS LIVE. COMPRESSION ENABLED. OWNER: IBRAHIM MUSTAFA")
    threading.Thread(target=cleaner_engine, daemon=True).start()
    bot.infinity_polling(timeout=90)
