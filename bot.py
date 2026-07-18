import discord
from discord.ext import commands
from discord.ui import Button, View
import json
import os
import random
import asyncio
import datetime

TOKEN = os.getenv('TOKEN')
PREFIX = '🔥'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f'🔥 Chaos of Wars جاهز!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ مثال: `🔥مبارزة @لاعب`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("⚠️ العضو غير موجود")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("⚠️ للمالك والمشرفين فقط")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send("⚠️ حدث خطأ، حاول مرة أخرى.")

# =================================================
# القائمة التفاعلية (UI)
# =================================================
class MainMenuView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="⚔️ المبارزة", style=discord.ButtonStyle.danger)
    async def duel_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("لعب المبارزة: اكتب `🔥مبارزة @اللاعب` لتحدي شخص.", ephemeral=True)

    @discord.ui.button(label="🎡 الروليت", style=discord.ButtonStyle.primary)
    async def roulette_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🎡 للعب الروليت: اكتب `🔥روليت`، ثم `🔥سجل`، ثم `🔥دور`.", ephemeral=True)

    @discord.ui.button(label="🛡️ المتجر", style=discord.ButtonStyle.success)
    async def shop_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🛡️ المتجر: اكتب `🔥متجر` لرؤية الأسعار.", ephemeral=True)

    @discord.ui.button(label="🎮 ألعاب ترفيهية", style=discord.ButtonStyle.secondary)
    async def games_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🎮 20 لعبة: اكتب `🔥العاب` لرؤية القائمة الكاملة.", ephemeral=True)

    @discord.ui.button(label="💰 نقاطي", style=discord.ButtonStyle.success)
    async def points_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("💰 لمعرفة النقاط: اكتب `🔥نقاطي`.", ephemeral=True)

# =================================================
# (1) القوانين التفاعلية (القصة + الأزرار)
# =================================================
@bot.command()
async def قوانين(ctx):
    story = """
**📜 ساحة الفوضى (Chaos of Wars Arena) 📜**

في عالمٍ لم يعد يعرف معنى العدالة، ظهرت منظمة غامضة تُدعى "النظام".
قررت هذه المنظمة بناء أعظم ساحة قتال تحت الأرض على الإطلاق.
أنت لست هنا بمحض إرادتك. لقد تم اختطافك، وتستيقظ لتجد نفسك داخل غرفة زجاجية معتمة.

*"مرحباً أيها المختار. القاعدة الوحيدة هنا هي: البقاء على قيد الحياة."*
    """
    embed = discord.Embed(title="🔥 قائمة الألعاب التفاعلية", description=story, color=0xff0000)
    embed.add_field(name="📜 ابدأ مغامرتك!", value="اختر ما تريد لعبه من الأزرار أدناه.", inline=False)
    view = MainMenuView()
    await ctx.send(embed=embed, view=view)

# =================================================
# (2) المتجر والنقاط
# =================================================
@bot.command()
async def متجر(ctx):
    embed = discord.Embed(title="🔥 متجر الفوضى", color=0xff0000)
    embed.add_field(name="🛡️ درع النجاة", value="3 نقاط", inline=False)
    embed.add_field(name="❄️ تجميد العجلة", value="5 نقاط", inline=False)
    embed.add_field(name="🧲 مغناطيس", value="4 نقاط", inline=False)
    embed.add_field(name="📡 رادار", value="6 نقاط", inline=False)
    embed.add_field(name="🎁 صندوق الجوائز", value="5 نقاط", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def نقاطي(ctx):
    uid = str(ctx.author.id)
    data = load_data()
    if uid not in data:
        data[uid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
        save_data(data)
    await ctx.send(f"🔥 نقاطك: **{data[uid]['points']}**")

@bot.command()
async def اشتري(ctx, *, item=None):
    uid = str(ctx.author.id)
    data = load_data()
    if uid not in data:
        data[uid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
    if item is None:
        await ctx.send("مثال: `🔥اشتري درع`")
        return
    prices = {"درع": 3, "تجميد": 5, "مغناطيس": 4, "رادار": 6}
    if item not in prices:
        await ctx.send("❌ غير موجود")
        return
    if data[uid]["points"] < prices[item]:
        await ctx.send("❌ نقاط غير كافية")
        return
    data[uid]["points"] -= prices[item]
    if item == "درع": data[uid]["shield"] += 1
    elif item == "تجميد": data[uid]["freeze"] += 1
    elif item == "مغناطيس": data[uid]["magnet"] += 1
    elif item == "رادار": data[uid]["radar"] += 1
    save_data(data)
    await ctx.send(f"✅ اشتريت **{item}**!")

# =================================================
# (3) الانضمام مع مكافأة خاصة
# =================================================
@bot.command()
async def انضم(ctx):
    uid = str(ctx.author.id)
    data = load_data()
    
    allowed_staff = [
        1504809491231801404,  # أنت (المالك King-of-Dragons)
        1146159441058746449,  # المشرف 1
        836777715708592129    # المشرف 2
    ]
    
    if uid not in data:
        if ctx.author.id in allowed_staff:
            data[uid] = {"points": 1000, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
            save_data(data)
            await ctx.send(f"👑 مرحباً أيها القائد {ctx.author.mention}! لقد حصلت على **1000 نقطة** مكافأة خاصة للمشرفين والمالك!")
        else:
            data[uid] = {"points": 100, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
            save_data(data)
            await ctx.send(f"🔥 مرحباً {ctx.author.mention}! لقد حصلت على **100 نقطة** لبدء رحلتك.")
    else:
        await ctx.send(f"🔥 {ctx.author.mention}، أنت مسجل بالفعل. رصيدك: {data[uid]['points']} نقطة.")

# =================================================
# (4) قائمة المتصدرين
# =================================================
@bot.command()
async def التوب(ctx):
    data = load_data()
    top = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True)[:5]
    embed = discord.Embed(title="🏆 أفضل 5", color=0xffd700)
    for i, (uid, info) in enumerate(top, 1):
        user = bot.get_user(int(uid))
        name = user.display_name if user else f"لاعب {i}"
        embed.add_field(name=f"{i}. {name}", value=f"{info['points']} نقطة", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def كافأ(ctx, member: discord.Member, amount: int):
    if ctx.author.id not in [1504809491231801404, 1146159441058746449, 836777715708592129]:
        await ctx.send("⚠️ للمالك والمشرفين فقط")
        return
    uid = str(member.id)
    data = load_data()
    if uid not in data:
        data[uid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
    data[uid]["points"] += amount
    save_data(data)
    await ctx.send(f"🎉 {member.mention} حصل على {amount} نقطة!")

# =================================================
# (5) الألعاب الرئيسية (المبارزة والروليت)
# =================================================
active_duels = {}

@bot.command()
async def مبارزة(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("❌ لا يمكن")
        return
    if ctx.author.id in active_duels:
        await ctx.send("⚠️ مشغول")
        return
    active_duels[ctx.author.id] = {"opponent": member.id, "accepted": False}
    await ctx.send(f"⚔️ {ctx.author.mention} يتحدى {member.mention}!\n`🔥قبول` للقبول.")

@bot.command()
async def قبول(ctx):
    challenger = None
    for cid, d in active_duels.items():
        if d["opponent"] == ctx.author.id:
            challenger = cid
            break
    if not challenger:
        await ctx.send("❌ لا يوجد تحدي")
        return
    active_duels[challenger]["accepted"] = True
    c1 = bot.get_user(challenger)
    winner = random.choice([c1, ctx.author])
    await ctx.send(f"⚔️ بدأت! الفائز: {winner.mention} (+2 نقطة)")
    wdb = load_data()
    wid = str(winner.id)
    if wid not in wdb:
        wdb[wid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
    wdb[wid]["points"] += 2
    save_data(wdb)
    del active_duels[challenger]

# إضافة الروليت والمحقق
@bot.command()
async def روليت(ctx):
    await ctx.send(f"🎡 **روليت الفوضى!**\nاكتب `🔥سجل` للمشاركة، ثم `🔥دور` للبدء.\n(سيتم اختيار قاتل سري، والباقي محققون!)")

@bot.command()
async def سجل(ctx):
    pass

@bot.command()
async def دور(ctx):
    await ctx.send(f"🎡 العجلة تدور... استخدم `🔥تحقق @الاسم` لكشف القاتل!")

@bot.command()
async def تحقق(ctx, member: discord.Member):
    await ctx.send(f"🕵️ التحقق من {member.mention}...")

# =================================================
# (6) الألعاب الترفيهية (20 لعبة)
# =================================================
@bot.command()
async def العاب(ctx):
    embed = discord.Embed(title="🎮 20 لعبة مسلية في البوت!", description="استمتع بمجموعة متنوعة من الألعاب", color=0x00ff00)
    embed.add_field(name="🪨 حجر ورقة مقص", value="`🔥حجر` + اختيارك", inline=False)
    embed.add_field(name="🪙 اقلب العملة", value="`🔥اقلب` + صورة/كتابة", inline=False)
    embed.add_field(name="🎲 نرد", value="`🔥نرد`", inline=False)
    embed.add_field(name="🔢 تخمين الرقم", value="`🔥تخمين` + رقم (1-10)", inline=False)
    embed.add_field(name="❓ سؤال", value="`🔥سؤال`", inline=False)
    embed.add_field(name="💬 اقتباس", value="`🔥اقتباس`", inline=False)
    embed.add_field(name="😂 نكتة", value="`🔥نكتة`", inline=False)
    embed.add_field(name="🪄 ساحر", value="`🔥ساحر` + سؤالك", inline=False)
    embed.add_field(name="🕐 الوقت", value="`🔥زمن`", inline=False)
    embed.add_field(name="🔢 بصمة", value="`🔥بصمة`", inline=False)
    embed.add_field(name="🔮 كرة", value="`🔥كرة` + سؤالك", inline=False)
    embed.add_field(name="🥊 تحدي", value="`🔥تحدي` @اللاعب", inline=False)
    embed.add_field(name="🔫 قاتل", value="`🔥قاتل`", inline=False)
    embed.add_field(name="🌀 مصير", value="`🔥مصير`", inline=False)
    embed.add_field(name="🌟 طالع", value="`🔥طالع`", inline=False)
    embed.add_field(name="🎨 لون", value="`🔥لون`", inline=False)
    embed.add_field(name="🐾 حيوان", value="`🔥حيوان`", inline=False)
    embed.add_field(name="🍔 غذاء", value="`🔥غذاء`", inline=False)
    embed.add_field(name="🍀 حظ", value="`🔥حظ`", inline=False)
    embed.add_field(name="✈️ رحلة", value="`🔥رحلة`", inline=False)
    await ctx.send(embed=embed)

# تنفيذ الألعاب الفردية
@bot.command()
async def حجر(ctx, choice: str = None):
    if choice is None:
        await ctx.send("اختر: `🔥حجر حجر` أو `🔥حجر ورقة` أو `🔥حجر مقص`")
        return
    options = ["حجر", "ورقة", "مقص"]
    bot_choice = random.choice(options)
    user_choice = choice.strip()
    if user_choice not in options:
        await ctx.send("اختر: حجر، ورقة، أو مقص")
        return
    if user_choice == bot_choice:
        result = "🤝 تعادل!"
    elif (user_choice == "حجر" and bot_choice == "مقص") or \
         (user_choice == "ورقة" and bot_choice == "حجر") or \
         (user_choice == "مقص" and bot_choice == "ورقة"):
        result = "🎉 فزت!"
    else:
        result = "💔 خسرت!"
    await ctx.send(f"🔥 أنت: {user_choice} | البوت: {bot_choice}\n{result}")

@bot.command()
async def اقلب(ctx, choice: str = None):
    if choice is None:
        await ctx.send("اختر: `🔥اقلب صورة` أو `🔥اقلب كتابة`")
        return
    options = ["صورة", "كتابة"]
    bot_choice = random.choice(options)
    user_choice = choice.strip()
    if user_choice not in options:
        await ctx.send("اختر: صورة أو كتابة")
        return
    if user_choice == bot_choice:
        result = "🎉 فزت!"
    else:
        result = "💔 خسرت!"
    await ctx.send(f"💰 أنت: {user_choice} | البوت: {bot_choice}\n{result}")

@bot.command()
async def نرد(ctx):
    await ctx.send(f"🎲 نرد البوت: **{random.randint(1, 6)}**!")

@bot.command()
async def تخمين(ctx, number: int = None):
    if number is None:
        await ctx.send("اختر رقم: `🔥تخمين 5`")
        return
    if number < 1 or number > 10:
        await ctx.send("اختر رقماً من 1 إلى 10")
        return
    bot_num = random.randint(1, 10)
    if number == bot_num:
        await ctx.send(f"🎉 فزت! رقم البوت كان {bot_num}!")
    else:
        await ctx.send(f"💔 خسرت! رقم البوت كان {bot_num}.")

@bot.command()
async def سؤال(ctx):
    questions = ["ما هو أطول نهر في العالم؟", "كم عدد الكواكب في المجموعة الشمسية？"]
    await ctx.send(f"❓ {random.choice(questions)}")

@bot.command()
async def اقتباس(ctx):
    quotes = ["النجاح ليس نهائياً، والفشل ليس قاتلاً.", "الحياة ليست مجرد العثور على نفسك."]
    await ctx.send(f"💬 {random.choice(quotes)}")

@bot.command()
async def نكتة(ctx):
    jokes = ["لماذا لا يلعب الكمبيوتر كرة القدم؟ لأنه يخاف من الفيروسات!"]
    await ctx.send(f"😂 {random.choice(jokes)}")

@bot.command()
async def ساحر(ctx, *, question: str = None):
    if question is None:
        await ctx.send("اكتب سؤالاً: `🔥ساحر هل سأفوز؟`")
        return
    answers = ["نعم", "لا", "ربما"]
    await ctx.send(f"🪄 {random.choice(answers)}")

@bot.command()
async def زمن(ctx):
    now = datetime.datetime.now()
    await ctx.send(f"🕐 الوقت: **{now.strftime('%H:%M')}**")

@bot.command()
async def بصمة(ctx):
    await ctx.send(f"🔢 بصمة: **{random.randint(100000, 999999)}**")

@bot.command()
async def كرة(ctx, *, question: str = None):
    if question is None:
        await ctx.send("اكتب سؤالاً: `🔥كرة هل سأنتصر؟`")
        return
    answers = ["نعم.", "لا.", "ربما."]
    await ctx.send(f"🔮 {random.choice(answers)}")

@bot.command()
async def تحدي(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("اذكر لاعباً: `🔥تحدي @لاعب`")
        return
    challenges = [f"{ctx.author.mention} يتحدى {member.mention} في مباراة رقص!"]
    await ctx.send(f"🥊 {random.choice(challenges)}")

@bot.command()
async def قاتл(ctx):
    await ctx.send("🔫 القاتل الصامت يضرب في الظلام...")

@bot.command()
async def مصير(ctx):
    await ctx.send(f"🌀 {random.choice(['أنت مكتوب لك النصر.', 'قدرك غامض.'])}")

@bot.command()
async def طالع(ctx):
    signs = ["الحمل", "الثور", "الجوزاء", "السرطان"]
    await ctx.send(f"🌟 طالعك: **{random.choice(signs)}**")

@bot.command()
async def لون(ctx):
    colors = ["أحمر", "أزرق", "أخضر"]
    await ctx.send(f"🎨 لونك: **{random.choice(colors)}**")

@bot.command()
async def حيوان(ctx):
    animals = ["أسد", "نمر", "فيل"]
    await ctx.send(f"🐾 حيوانك: **{random.choice(animals)}**")

@bot.command()
async def غذاء(ctx):
    foods = ["بيتزا", "برغر", "سوشي"]
    await ctx.send(f"🍔 الغذاء: **{random.choice(foods)}**")

@bot.command()
async def حظ(ctx):
    await ctx.send(f"🍀 حظك: **{random.randint(0, 100)}%**")

@bot.command()
async def رحلة(ctx):
    destinations = ["باريس", "طوكيو", "نيويورك"]
    await ctx.send(f"✈️ وجهتك: **{random.choice(destinations)}**")

# =================================================
# تشغيل البوت
# =================================================
if __name__ == "__main__":
    if TOKEN is None:
        print("❌ التوكن مفقود!")
    else:
        bot.run(TOKEN)@bot.command()
async def متجر(ctx):
    embed = discord.Embed(title="🔥 متجر الفوضى", color=0xff0000)
    embed.add_field(name="🛡️ درع النجاة", value="3 نقاط (ينقذك من الموت)", inline=False)
    embed.add_field(name="❄️ تجميد العجلة", value="5 نقاط (يفوز لك بالروليت)", inline=False)
    embed.add_field(name="🎁 صندوق الجوائز", value="5 نقاط (جائزة عشوائية)", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def نقاطي(ctx):
    uid = str(ctx.author.id)
    data = load_data()
    if uid not in data:
        data[uid] = {"points": 0, "shield": 0, "freeze": 0}
        save_data(data)
    await ctx.send(f"🔥 **{ctx.author.display_name}**، رصيدك الحالي: **{data[uid]['points']}** نقطة.")

@bot.command()
async def اشتري(ctx, *, item=None):
    uid = str(ctx.author.id)
    data = load_data()
    if uid not in data:
        data[uid] = {"points": 0, "shield": 0, "freeze": 0}
    if item is None:
        await ctx.send("⚠️ مثال: `🔥اشتري درع`")
        return
    prices = {"درع": 3, "تجميد": 5}
    if item not in prices:
        await ctx.send("❌ هذا العنصر غير موجود!")
        return
    if data[uid]["points"] < prices[item]:
        await ctx.send(f"❌ نقاط غير كافية! تحتاج {prices[item]} نقطة.")
        return
    data[uid]["points"] -= prices[item]
    if item == "درع":
        data[uid]["shield"] += 1
    elif item == "تجميد":
        data[uid]["freeze"] += 1
    save_data(data)
    await ctx.send(f"✅ اشتريت **{item}** بنجاح!")

# =================================================
# (3) أمر الانضمام
# =================================================
@bot.command()
async def انضم(ctx):
    uid = str(ctx.author.id)
    data = load_data()
    if uid not in data:
        data[uid] = {"points": 100, "shield": 0, "freeze": 0}
        save_data(data)
        await ctx.send(f"🔥 مرحباً {ctx.author.mention}! لقد حصلت على **100 نقطة** لبدء رحلتك.")
    else:
        await ctx.send(f"🔥 {ctx.author.mention}، أنت مسجل بالفعل. رصيدك: {data[uid]['points']} نقطة.")

# =================================================
# (4) قائمة المتصدرين
# =================================================
@bot.command()
async def التوب(ctx):
    data = load_data()
    sorted_users = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True)[:5]
    embed = discord.Embed(title="🏆 قاعة المشاهير (أفضل 5)", color=0xffd700)
    for idx, (user_id, info) in enumerate(sorted_users, 1):
        user = bot.get_user(int(user_id))
        name = user.display_name if user else f"لاعب {idx}"
        embed.add_field(name=f"{idx}. {name}", value=f"⭐ {info['points']} نقطة", inline=False)
    await ctx.send(embed=embed)

# =================================================
# (5) نظام المبارزة
# =================================================
active_duels = {}

@bot.command()
async def مبارزة(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("❌ لا يمكنك مبارزة نفسك!")
        return
    if ctx.author.id in active_duels:
        await ctx.send("⚠️ أنت مشغول بمبارزة حالياً.")
        return
    active_duels[ctx.author.id] = {"opponent": member.id, "accepted": False}
    await ctx.send(f"⚔️ {ctx.author.mention} يتحدى {member.mention}!\n`🔥قبول` للقبول. لديك 60 ثانية.")

@bot.command()
async def قبول(ctx):
    challenger_id = None
    for cid, data in active_duels.items():
        if data["opponent"] == ctx.author.id:
            challenger_id = cid
            break
    if challenger_id is None:
        await ctx.send("❌ لا يوجد تحدٍ لك حالياً.")
        return
    active_duels[challenger_id]["accepted"] = True
    challenger = bot.get_user(challenger_id)
    await ctx.send(f"⚔️ المبارزة بدأت بين {challenger.mention} و {ctx.author.mention}!")
    winner = random.choice([challenger, ctx.author])
    await asyncio.sleep(3)
    await ctx.send(f"🏆 الفائز هو **{winner.mention}**! حصل على نقطتين!")
    w_uid = str(winner.id)
    db = load_data()
    if w_uid not in db:
        db[w_uid] = {"points": 100, "shield": 0, "freeze": 0}
    db[w_uid]["points"] += 2
    save_data(db)
    del active_duels[challenger_id]

# =================================================
# (6) صندوق الجوائز
# =================================================
@bot.command()
async def صندوق(ctx):
    uid = str(ctx.author.id)
    data = load_data()
    if uid not in data:
        data[uid] = {"points": 0, "shield": 0, "freeze": 0}
    if data[uid]["points"] < 5:
        await ctx.send("❌ نقاط غير كافية! الصندوق يكلف 5 نقاط.")
        return
    data[uid]["points"] -= 5
    prizes = [
        ("نقطة", 10),
        ("نقطة", 5),
        ("درع", 1),
        ("تجميد", 1),
    ]
    prize_name, prize_amount = random.choice(prizes)
    if prize_name == "نقطة":
        data[uid]["points"] += prize_amount
        await ctx.send(f"🎁 ربحت **{prize_amount} نقطة**!")
    elif prize_name == "درع":
        data[uid]["shield"] += 1
        await ctx.send("🎁 ربحت **🛡️ درعاً**!")
    elif prize_name == "تجميد":
        data[uid]["freeze"] += 1
        await ctx.send("🎁 ربحت **❄️ تجميذاً**!")
    save_data(data)

# =================================================
# (7) نظام المكافآت (للمالك والمشرفين فقط)
# =================================================
@bot.command()
async def كافأ(ctx, member: discord.Member, amount: int):
    # قائمة المعرفات المسموح لها باستخدام الأمر (المالك + المشرفين)
    allowed_users = [
        1504809491231801404,  # أنت (King-of-Dragons)
        1146159441058746449,  # المشرف 1
        836777715708592129    # المشرف 2
    ]
    
    if ctx.author.id not in allowed_users:
        await ctx.send("⚠️ هذا الأمر للمالك والمشرفين فقط.")
        return
    uid = str(member.id)
    data = load_data()
    if uid not in data:
        data[uid] = {"points": 0, "shield": 0, "freeze": 0}
    data[uid]["points"] += amount
    save_data(data)
    await ctx.send(f"🎉 {member.mention} حصل على **{amount} نقطة**!")

# =================================================
# (8) لعبة الروليت التفاعلية + المحقق
# =================================================
roulette_players = []
detective_mode = {}

@bot.command()
async def روليت(ctx):
    global roulette_players, detective_mode
    roulette_players = []
    detective_mode = {}
    await ctx.send(f"🎡 **روليت الفوضى!**\nاكتب `🔥سجل` للمشاركة، ثم `🔥دور` للبدء.\n(سيتم اختيار قاتل سري، والباقي محققون!)")

@bot.command()
async def سجل(ctx):
    if ctx.author not in roulette_players:
        roulette_players.append(ctx.author)
        await ctx.send(f"✅ {ctx.author.mention} سجل! ({len(roulette_players)} لاعب)")
    else:
        await ctx.send("❌ أنت مسجل بالفعل!")

@bot.command()
async def دور(ctx):
    global roulette_players, detective_mode
    if len(roulette_players) < 2:
        await ctx.send("❌ يجب أن يكون لاعبين على الأقل!")
        return
    killer = random.choice(roulette_players)
    detective_mode["killer"] = killer.id
    await ctx.send(f"🎡 العجلة تدور...")
    await asyncio.sleep(2)
    chosen = random.choice(roulette_players)
    await ctx.send(f"⏹️ العجلة توقفت عند: {chosen.mention}")
    data = load_data()
    cid = str(chosen.id)
    if cid not in data:
        data[cid] = {"points": 0, "shield": 0, "freeze": 0}
    if data[cid].get("freeze", 0) > 0:
        data[cid]["freeze"] -= 1
        save_data(data)
        await ctx.send(f"❄️ {chosen.mention} يستخدم التجميد!\n`🔥اطرد @الاسم` لطرد لاعب")
    else:
        await ctx.send(f"🎯 {chosen.mention}، اختر:\n`🔥اطرد @الاسم` أو `🔥عشوائي` أو `🔥تحقق @الاسم`")

@bot.command()
async def تحقق(ctx, member: discord.Member):
    if ctx.author not in roulette_players:
        await ctx.send("❌ أنت لست في اللعبة!")
        return
    if ctx.author.id == detective_mode.get("killer"):
        await ctx.send("❌ القاتل لا يمكنه التحقق من نفسه!")
        return
    if member.id == detective_mode.get("killer"):
        await ctx.send(f"🕵️ **تحذير! {member.mention} هو القاتل!**")
    else:
        await ctx.send(f"✅ {member.mention} ليس القاتل.")

@bot.command()
async def اطرد(ctx, member: discord.Member):
    if ctx.author not in roulette_players:
        await ctx.send("❌ أنت لست في اللعبة!")
        return
    data = load_data()
    mid = str(member.id)
    if mid not in data:
        data[mid] = {"points": 0, "shield": 0, "freeze": 0}
    if data[mid].get("shield", 0) > 0:
        data[mid]["shield"] -= 1
        save_data(data)
        await ctx.send(f"🛡️ **{member.mention} نجا!** درعه تحطم.")
    else:
        roulette_players.remove(member)
        await ctx.send(f"💀 **{member.mention} تم طرده!**")
        wid = str(ctx.author.id)
        if wid not in data:
            data[wid] = {"points": 0, "shield": 0, "freeze": 0}
        data[wid]["points"] += 2
        save_data(data)
        await ctx.send(f"🏆 {ctx.author.mention} ربح **2 نقطة**!")

@bot.command()
async def عشوائي(ctx):
    if ctx.author not in roulette_players:
        await ctx.send("❌ أنت لست في اللعبة!")
        return
    victims = [p for p in roulette_players if p != ctx.author]
    if not victims:
        await ctx.send("❌ لا يوجد أحد لتطرده!")
        return
    victim = random.choice(victims)
    data = load_data()
    vid = str(victim.id)
    if vid not in data:
        data[vid] = {"points": 0, "shield": 0, "freeze": 0}
    if data[vid].get("shield", 0) > 0:
        data[vid]["shield"] -= 1
        save_data(data)
        await ctx.send(f"🛡️ العجلة اختارت {victim.mention}، لكن درعه حماه!")
    else:
        roulette_players.remove(victim)
        await ctx.send(f"🎲 **{victim.mention} طُرد عشوائياً!**")
        wid = str(ctx.author.id)
        if wid not in data:
            data[wid] = {"points": 0, "shield": 0, "freeze": 0}
        data[wid]["points"] += 2
        save_data(data)
        await ctx.send(f"🏆 {ctx.author.mention} ربح **2 نقطة**!")

# =================================================
# (9) تشغيل البوت
# =================================================
if __name__ == "__main__":
    if TOKEN is None:
        print("❌ التوكن مفقود!")
    else:
        bot.run(TOKEN)# (4) أمر بدء تشغيل البوت
# =============================================
@bot.event
async def on_ready():
    print(f'✅ Chaos of Wars bot is online!')

# =============================================
# (5) قصة ساحة الفوضى (الأمر RHCOWrules)
# =============================================
@bot.command()
async def rules(ctx):
    story = """
    **📜 ساحة الفوضى (Chaos of Wars Arena) 📜**

    في عالمٍ لم يعد يعرف معنى العدالة، ظهرت منظمة غامضة تُدعى "النظام".
    قررت هذه المنظمة بناء أعظم ساحة قتال تحت الأرض على الإطلاق.
    أنت لست هنا بمحض إرادتك. لقد تم اختطافك، وتستيقظ لتجد نفسك داخل غرفة زجاجية معتمة.

    *"مرحباً أيها المختار. القاعدة الوحيدة هنا هي: البقاء على قيد الحياة."*

    تم تسليمك 100 قطعة نقدية من عملة الساحة (عملات RH).
    **🛡️ درع النجاة (Shield):** يحميك من رصاصة واحدة (السعر: 50 قطعة).
    **💣 قنبلة الفوضى (Grenade):** تقتل خصمك فوراً (السعر: 75 قطعة).

    **اكتب `RHCOWplay` وابدأ رحلتك نحو الموت... أو نحو الخلود.**
    """
    await ctx.send(story)

# =============================================
# (6) نظام المتجر والنقود
# =============================================
@bot.command()
async def shop(ctx):
    embed = discord.Embed(title="🏪 متجر ساحة الفوضى", color=0x00ff00)
    embed.add_field(name="🛡️ درع النجاة", value="السعر: 50 قطعة", inline=False)
    embed.add_field(name="💣 قنبلة الفوضى", value="السعر: 75 قطعة", inline=False)
    embed.set_footer(text="للشراء: RHCOWbuy [اسم العنصر]")
    await ctx.send(embed=embed)

@bot.command()
async def coins(ctx):
    user_id = str(ctx.author.id)
    data = load_data()
    if user_id not in data:
        data[user_id] = {"coins": 100, "shield": 0, "grenade": 0}
        save_data(data)
    await ctx.send(f"💰 {ctx.author.mention}، رصيدك الحالي: **{data[user_id]['coins']}** قطعة.")

@bot.command()
async def buy(ctx, *, item=None):
    user_id = str(ctx.author.id)
    data = load_data()
    if user_id not in data:
        data[user_id] = {"coins": 100, "shield": 0, "grenade": 0}
    
    if item is None:
        await ctx.send("❌ مثال للشراء: `RHCOWbuy درع`")
        return
    
    prices = {"درع": 50, "قنبلة": 75}
    if item not in prices:
        await ctx.send("❌ هذا العنصر غير موجود في المتجر!")
        return
    
    price = prices[item]
    if data[user_id]["coins"] < price:
        await ctx.send(f"❌ ليس لديك نقود كافية! تحتاج **{price}** قطعة.")
        return
    
    data[user_id]["coins"] -= price
    if item == "درع":
        data[user_id]["shield"] += 1
    elif item == "قنبلة":
        data[user_id]["grenade"] += 1
    
    save_data(data)
    await ctx.send(f"✅ اشتريت **{item}** بنجاح! الرصيد المتبقي: {data[user_id]['coins']} قطعة.")

# =============================================
# (7) لعبة الروليت (فوضى الحرب)
# =============================================
@bot.command()
async def play(ctx):
    user_id = str(ctx.author.id)
    data = load_data()
    if user_id not in data:
        data[user_id] = {"coins": 100, "shield": 0, "grenade": 0}
        save_data(data)

    await ctx.send(f"🔫 **{ctx.author.mention} انضم إلى ساحة الفوضى!** (يجب أن يكون شخصين للعب).\nاكتب `RHCOWstart` لبدء المعركة.")

@bot.command()
async def start(ctx):
    # جلب الأعضاء غير البوتات
    members = [m for m in ctx.guild.members if not m.bot]
    if len(members) < 2:
        await ctx.send("❌ لا يوجد لاعبين كافيين! يجب أن يكون شخصين على الأقل.")
        return
    
    killer = random.choice(members)
    victim = random.choice([m for m in members if m != killer])
    
    await ctx.send(f"⏳ جاري اختيار القاتل...")
    await asyncio.sleep(2)
    await ctx.send(f"🔫 **القاتل الصامت هو: {killer.mention}**")
    await asyncio.sleep(2)
    await ctx.send(f"🎯 القاتل يوجه مسدسه نحو {victim.mention}...")
    await asyncio.sleep(2)
    
    # التحقق من الدرع
    data = load_data()
    if str(victim.id) not in data:
        data[str(victim.id)] = {"coins": 100, "shield": 0, "grenade": 0}
    
    if data[str(victim.id)].get("shield", 0) > 0:
        data[str(victim.id)]["shield"] -= 1
        save_data(data)
        await ctx.send(f"🛡️ **لقد نجا {victim.mention}!** درعه تحطم لكنه بقي حياً!")
    else:
        await ctx.send(f"💀 **لقد قُتل {victim.mention}!** خارج ساحة الفوضى!")
        # إعطاء مكافأة للقاتل
        if str(killer.id) not in data:
            data[str(killer.id)] = {"coins": 100, "shield": 0, "grenade": 0}
        data[str(killer.id)]["coins"] += 50
        save_data(data)
        await ctx.send(f"🏆 {killer.mention} ربح المعركة وحصل على **50 قطعة** إضافية!")

# =============================================
# (8) تشغيل البوت
# =============================================
if __name__ == "__main__":
    if TOKEN is None:
        print("❌ خطأ: لم يتم العثور على التوكن! تأكد من إضافته في Environment Variables في Render.")
    else:
        bot.run(TOKEN)
