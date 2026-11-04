import discord
from discord.ext import commands
import re
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# قائمة الدومينات أو الروابط المشبوهة الممنوعة (يمكنك إضافتها أو تعديلها هنا)
BLOCKED_DOMains = [
    "free-nitro",
    "discord-gifts",
    "steam-nitro",
    "free-robux",
    "nitro-discord",
]

# تعبير نمطي (Regex) لاكتشاف الروابط بشكل عام
URL_PATTERN = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # التحقق من وجود روابط أو دومينات مشبوهة في الرسالة
    content = message.content.lower()
    
    # فحص الدومينات الممنوعة محددة الهدف
    is_blocked = any(domain in content for domain in BLOCKED_DOMains)
    
    # أو فحص الروابط العامة إذا أردت تفعيلها (مغلقة حالياً للاكتفاء بالمشبوهة فقط، أو افتحها حسب رغبتك)
    # has_url = URL_PATTERN.search(content)

    if is_blocked:
        try:
            await message.delete()
            warning_msg = await message.channel.send(
                f"⚠️ {message.author.mention}, ممنوع إرسال روابط أو دومينات مشبوهة في هذا السيرفر!"
            )
            # حذف رسالة التحذير بعد 5 ثوانٍ لتنظيف الشات
            await warning_msg.delete(delay=5)
        except Exception as e:
            print(f"خطأ أثناء حذف الرسالة: {e}")

    await bot.process_commands(message)

# تشغيل البوت باستخدام التوكن من البيئة
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("خطأ: لم يتم العثور على متغير البيئة DISCORD_TOKEN!")
