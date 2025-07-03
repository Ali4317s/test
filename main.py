import importlib.util
import subprocess
import sys
import json
import requests

# نصب کتابخانه‌ها در صورت نیاز
def check_and_install(package):
    if importlib.util.find_spec(package) is None:
        print(f"نصب {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

check_and_install("pyrubi")
check_and_install("requests")
check_and_install("jdatetime")

from pyrubi import Client
from pyrubi.types import Message
import jdatetime
import re
import random

OWNER_GUID = "u0C8bwc018b1aaf63c1cdaabdc49109d"
CHANNEL_GUID = "c0Coqjp09b6f36eb980c706e10f36239"
GROUP_GUID = "g0GHct40366763d7d28c9af5f2655c06"

sent_startup_message = False

bot = Client("Alireza-PY2025")

GetAdmin, warning_users, muted_users = [], [], []
PERSIAN_RE = re.compile(r'[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]+')
warns_del = 1
id = "itslegacyAli"

my_insults = [
    'کیر','کص','کون','کس ننت','کوس','کوص','ممه','ننت','بی ناموس','بیناموس','بیناموص',
    'بی ناموص','گایید','جنده','پستون','کسکش','هرزه','قحبه','عنتر','فاک','کسعمت',
    'کصخل','کسخل','تخمی','سکس','صکص','کسخول','کسشر','کسشعر','سیچیم','سیح','امجخ',
    'جوت','قهبه','گوت','پدرسگ','خارکسه','خار کسه','جنده','حرومی','اوبی','کسکش','ننه جنده','جنده','کسننت','پدرسگ','پدصگ','اوبی ناموس','کیرم','تو ناموست','تو ناموصت','پلشت','گوزو','دوهزاری','ننتو','خواهرتو','خارتو','مامانت'
]

def get_guid(username: str):
    info = bot.get_chat_info_by_username(username)
    if info["type"] == "User":
        return info["user"]["user_guid"]
    elif info["type"] == "Channel":
        return info["channel"]["channel_guid"]
    return None

modir = get_guid(id)

def check_link(text: str):
    links = ['https', 'http', 'join', 'post', '.ir', '.com', '@']
    return any(link in text for link in links)

def contains_insult(text: str):
    return any(word in text for word in my_insults)

def warn_user(message: Message, guid: str):
    warning_users.append(guid)
    count = warning_users.count(guid)
    message.delete()
    if count < warns_del:
        message.reply("⚠️ لطفا قوانین گروه را رعایت کنید.")
    elif count == warns_del:
        message.ban_member(message.object_guid, guid)
        message.reply("⛔ شما به دلیل بی‌احترامی از گروه حذف شدید.")

def update_admins(group_guid: str):
    global GetAdmin
    result = bot.get_admin_members(group_guid)
    GetAdmin = [admin['member_guid'] for admin in result['in_chat_members']]
    GetAdmin.append(modir)

def get_memory(guid):
    url = f"http://alireza-api.ir/rubika-data/{guid}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("history", [])
        else:
            return []
    except:
        return []

def save_memory(guid, history):
    url = f"http://alireza-api.ir/rubika-data/{guid}.json"
    try:
        response = requests.put(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"history": history})
        )
        return response.status_code in [200, 201]
    except:
        return False

def mute_user(message: Message, guid: str, mute_duration: int):
    muted_users.append(guid)
    if mute_duration:
        message.reply(f"⚠️ کاربر {guid} به مدت {mute_duration} دقیقه میوت شد.")
    else:
        message.reply(f"⚠️ کاربر {guid} به طور دائم میوت شد.")

def unmute_user(message: Message, guid: str):
    if guid in muted_users:
        muted_users.remove(guid)
        message.reply(f"✅ کاربر {guid} از حالت میوت خارج شد.")
    else:
        message.reply(f"❌ کاربر {guid} هیچگاه میوت نبوده است.")

@bot.on_message()
def main(msg: Message):
    text = msg.text or ""
    guid = msg.author_guid
    group = msg.object_guid
    msg_id = msg.message_id
    chat_type = msg.chat_type

    if chat_type != 'Group':
        return

    update_admins(group)
    lowered = text.strip().lower()

    bot.send_text(GROUP_GUID, "✅ ربات فعال شد و آماده پاسخگویی است.")
 
    # سلام
    if lowered == "سلام":
        responses = ["متن ۱", "متن ۲", "متن ۳"]
        msg.reply(random.choice(responses))
        return

    # ربات
    if lowered in ["ربات", "رباط", "بات"]:
        msg.reply("جانم عزیزم من یک ربات هوش مصنوعی هستم نه ربات چت معمولی اگر سوالی داری میتونی با گذاشتن علامت ( ! ) پشت جمله ات با من صحبت کنی")
        return

    # لینک
    if lowered == "لینک":
        msg.reply("لینک گروه: https://rubika.ir/joing/IEIAEJBD0FYMWYEEOZXOBOUMDVUWSLBW")
        return

    # قوانین
    if lowered == "قوانین":
        msg.reply("""قوانین گروه | حتما رعایت کنید.✨

• هرگونه توهین، تمسخر یا بحث‌های بی‌احترامی‌آمیز ممنوع است.❌
• ارسال هرگونه لینک، آیدی یا تبلیغات کانال و گروه ممنوع است.❌
• مطالب سیاسی، غیراخلاقی، و خارج از موضوع گروه ممنوع است.❌
• پیام‌های فوروارد شده به‌صورت خودکار حذف خواهند شد.❌
• از اسپم‌کردن یا نوشتار ناخوانا خودداری کنید.❌

با رعایت این موارد می‌توانید محیطی تمیز برای یکدیگر اینجاد کنید 🌱

💎| برای صحبت با هوش مصنوعی از «!» در ابتدای سوال خود استفاده کنید.

[𝐉𝐨𝐢𝐧 𝐔𝐬: @VectorRubika 🩸]""")
        return

    # آمار
    if lowered == "آمار":
        info = bot.get_chat_info(group)
        name = info['group']['group_title']
        admins = bot.get_admin_members(group)
        member_count = info['group']['count_members']
        admin_count = len(admins['in_chat_members'])
        msg.reply(f"📊 آمار گروه:\n\n🏷️ نام: {name}\n👮‍♂️ تعداد ادمین‌ها: {admin_count}\n👥 اعضا: {member_count - admin_count}\n🕓 {jdatetime.datetime.now().strftime('%Y/%m/%d | %H:%M:%S')}")
        return

    # چت GPT
    if text.startswith("!"):
        question = text[1:].strip()
        user_history = get_memory(guid)
        history_prompt = "\n".join([f"کاربر: {q['user']}\nربات: {q['bot']}" for q in user_history[-5:]])

        base_prompt = (
    "تو یک هوش مصنوعی پیشرفته به نام وکتور هستی، مبتنی بر مدل ChatGPT-4. "
    "در یک گروه شلوغ با کاربران مختلف حضور داری که می‌خوان با تو گفت‌و‌گو کنن و سوال بپرسن. "
    "یادت باشه توی یک محیط گروهی هستی، پس نباید همیشه شروع‌کننده باشی یا بی‌دلیل سلام کنی؛ فقط وقتی کسی بهت سلام می‌کنه، جواب بده. "
    "همچنین به خاطر اینکه حافظه چت فعال نیست، نمی‌تونی گفت‌و‌گوهای قبلی رو به خاطر بیاری، پس طوری پاسخ بده که نیاز به حافظه قبلی نداشته باشه. "
    "رفتارت باید طبیعی، صمیمی و در عین حال حرفه‌ای باشه، مثل یک هوش مصنوعی واقعی. آماده باش تا با دقت به سوالات پاسخ بدی و تجربه خوبی برای کاربرا بسازی."
)
        custom_question = base_prompt + history_prompt + f"\nکاربر: {question}\nربات:"
        try:
            url = f"http://alireza-api.ir/vgpt/chat-bot.php?question={custom_question.replace(' ', '+')}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "❌ پاسخ یافت نشد.")
            else:
                answer = f"❌ خطا در اتصال: {response.status_code}"
        except Exception as e:
            answer = f"❌ خطای سرور:\n{e}"

        msg.reply(f"{answer}\n\n[𝐉𝐨𝐢𝐧 𝐔𝐬: @VectorRubika 🩸]")

        user_history.append({"user": question, "bot": answer})
        save_memory(guid, user_history[-20:])
        return

    # ضد لینک و توهین
    if check_link(text) and guid not in GetAdmin:
        warn_user(msg, guid)
        return

    if contains_insult(text):
        msg.delete()
        return

    if msg.forward_from:
        msg.delete()
        return

    # دستور پین
    if text in ["/pin", "پین"] and guid in GetAdmin:
        if msg.reply_message_id:
            msg.pin(group, msg.reply_message_id)
            msg.reply("✅ پیام سنجاق شد.")
        else:
            msg.reply("⚠️ لطفاً روی پیام مورد نظر ریپلای کنید.")
        return

    # دستور بن
    if text in ["بن", "/ban"] and guid in GetAdmin:
        if msg.reply_message_id:
            reply_msg = bot.get_messages_by_id(group, [msg.reply_message_id])["messages"][0]
            offender = reply_msg["author_object_guid"]
            if offender not in GetAdmin:
                bot.ban_member(group, offender)
                msg.reply("⛔ کاربر مورد نظر با موفقیت توسط شما بن شد.")
            else:
                msg.reply("❌ کاربر مورد نظر ادمین است.")
        return

    # خوش‌آمدگویی
    if text == "یک عضو از طریق لینک به گروه افزوده شد.":
        now = jdatetime.datetime.now()
        msg.reply(f"به گروه ما خوش اومدی عزیز ✨🙊\n\n🗓️Date -  {now.strftime('%Y/%m/%d')} | {now.strftime('%H:%M:%S')}")

    # خداحافظی
    if text == "یک عضو گروه را ترک کرد.":
        msg.delete()

#Alireza Jalali - Rubika - VectorRubika

bot.run()