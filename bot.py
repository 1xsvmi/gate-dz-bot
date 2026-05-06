import telebot
import requests
from bs4 import BeautifulSoup
import re

TOKEN = "8721409307:AAEAbw8lQfy77r1ppEiNLFEJF6VW_PoZm4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: 'aliexpress.com' in m.text.lower())
def handle_link(message):
    link = message.text.strip()
    try:
        match = re.search(r'/item/(\d+)', link)
        if not match:
            bot.reply_to(message, "يا خويا أرسل رابط منتج صحيح من علي إكسبريس")
            return
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(link, headers=headers, timeout=12)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        title = soup.find('h1').get_text(strip=True)[:70] if soup.find('h1') else "منتج علي إكسبريس"
        price = "تحقق من الصفحة"
        price_tag = soup.find('span', class_='notranslate') or soup.find('div', {'class': lambda x: x and 'price' in str(x).lower()})
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

print("Gate_Dz_Bot شغال...")
bot.polling()
