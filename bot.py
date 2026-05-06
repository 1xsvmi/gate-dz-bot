import telebot
import requests
import hashlib
import time
import json
import re

# ==================== إعداداتك ====================
TELEGRAM_TOKEN = "8721409307:AAEAbW8lQfy77r1ppEiNlFEJFt6VW_PoZm4"
APP_KEY = "533600"
APP_SECRET = "NHU8RehSTyMwwv7O5gdZVXupWUymYmYd"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generate_sign(params):
    sorted_params = sorted(params.items())
    sign_str = APP_SECRET + ''.join([f"{k}{v}" for k, v in sorted_params]) + APP_SECRET
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

def call_aliexpress_api(method, params):
    url = "https://api.aliexpress.com/sync"
    params["app_key"] = APP_KEY
    params["method"] = method
    params["timestamp"] = str(int(time.time() * 1000))
    params["sign_method"] = "md5"
    params["v"] = "2.0"
    params["format"] = "json"
    params["sign"] = generate_sign(params)
    
    response = requests.post(url, data=params, timeout=15)
    return response.json()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ أرسل رابط منتج من علي إكسبريس وسأعطيك أفضل 3 عروض + الشحن للجزائر + رابط affiliate")

@bot.message_handler(func=lambda m: 'aliexpress.com' in m.text.lower())
def handle_link(message):
    link = message.text.strip()
    try:
        product_id = re.search(r'/item/(\d+)', link).group(1)
        
        # 1. جلب تفاصيل المنتج
        detail_params = {
            "product_ids": product_id,
            "ship_to_country": "DZ",
            "target_currency": "USD",
            "target_language": "EN"
        }
        detail_result = call_aliexpress_api("aliexpress.affiliate.productdetail.get", detail_params)
        
        # 2. البحث عن أفضل 3 عروض
        search_params = {
            "keywords": "aliexpress",
            "sort": "priceAsc",
            "ship_to_country": "DZ",
            "target_currency": "USD",
            "page_size": "3"
        }
        search_result = call_aliexpress_api("aliexpress.affiliate.product.query", search_params)
        
        # بناء الرد
        reply = "✅ أفضل 3 عروض للجزائر:\n\n"
        
        # هنا نضيف المنطق لعرض النتائج (مبسط)
        reply += f"رابط المنتج: {link}\n"
        reply += "الشحن: تحقق من الروابط أدناه\n\n"
        reply += "🔥 استخدم الروابط أدناه لتربح أنا وأنت توفر"
        
        bot.reply_to(message, reply)
        
    except Exception as e:
        bot.reply_to(message, "فيه مشكل شوية، جرب رابط آخر")

print("البوت شغال مع AliExpress Affiliate API...")
bot.polling(none_stop=True)
