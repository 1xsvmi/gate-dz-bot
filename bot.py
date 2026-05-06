import telebot
import requests
from bs4 import BeautifulSoup
import re

# ==================== توكن البوت (مدمج) ====================
TOKEN = "8721409307:AAEAbW8lQfy77r1ppEiNlFEJFt6VW_PoZm4"
bot = telebot.TeleBot(TOKEN)
BOT_NAME = "Gate_Dz_Bot"

# ==================== رسالة الترحيب ====================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """✅ مرحبا بك في بوت Gate_Dz_Bot!

أرسل لي أي رابط منتج من علي إكسبريس وسأعطيك:
- السعر بالدولار (USD)
- معلومات الشحن للجزائر
- أفضل العروض

جرب الآن وأرسل رابط!"""
    bot.reply_to(message, welcome_text)

# ==================== معالج الروابط ====================
@bot.message_handler(func=lambda message: 'aliexpress.com' in message.text.lower())
def handle_product_link(message):
    link = message.text.strip()
    
    try:
        match = re.search(r'/item/(\d+)', link)
        if not match:
            bot.reply_to(message, "يا خويا أرسل رابط منتج صحيح من علي إكسبريس")
            return

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(link, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True)[:75] if title_tag else "منتج علي إكسبريس"

        price = "غير معروف"
        price_tag = soup.find('span', class_='notranslate') or soup.find('div', class_='product-price-current')
        if price_tag:
            price = price_tag.get_text(strip=True)

        reply = f"""✅ يا خويا لقيت لك:

📦 {title}
💵 السعر: {price} (بالدولار USD)
🚚 الشحن للجزائر: غالباً مجاني أو رخيص

🔥 رابط الشراء:
{link}

إذا تبي أفضل 3 عروض أرسل "بحث" + اسم المنتج

البوت مجاني - شاركو مع أصحابك!"""

        bot.reply_to(message, reply)

    except:
        bot.reply_to(message, "يا خويا فيه مشكل شوية، جرب رابط آخر.")

# ==================== تشغيل البوت ====================
print(f"{BOT_NAME} شغال بنجاح...")
bot.polling(none_stop=True)
