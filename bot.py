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
    embed = discord.Embed(title="🔥 قائمة الألعاب التفاعلية", description=story, color=0x220000)
    embed.add_field(name="📜 ابدأ مغامرتك!", value="اختر ما تريد لعبه من الأزرار أدناه.", inline=False)
    view = MainMenuView()
    await ctx.send(embed=embed, view=view)

# =================================================
# (2) المتجر والنقاط
# =================================================
@bot.command()
async def متجر(ctx):
    embed = discord.Embed(title="🔥 متجر الفوضى", color=0x330000)
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
        1504809491231801404,  # أنت (King-of-Dragons)
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

# =================================================
# (5) نظام المكافآت (للمالك والمشرفين فقط)
# =================================================
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
# (6) الألعاب الرئيسية (المبارزة والروليت)
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
    await ctx.send(f"⚔️ {ctx.author.mention} يتحدى {member.mention}!\n`🔥قبول` للقبول.")

@bot.command()
async def قبول(ctx):
    challenger = None
    for cid, d in active_duels.items():
        if d["opponent"] == ctx.author.id:
            challenger = cid
            break
    if not challenger:
        await ctx.send("❌ لا يوجد تحدي لك حالياً.")
        return
    active_duels[challenger]["accepted"] = True
    c1 = bot.get_user(challenger)
    winner = random.choice([c1, ctx.author])
    await ctx.send(f"⚔️ بدأت المبارزة! الفائز: **{winner.mention}** (+2 نقطة)")
    wdb = load_data()
    wid = str(winner.id)
    if wid not in wdb:
        wdb[wid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
    wdb[wid]["points"] += 2
    save_data(wdb)
    del active_duels[challenger]

# -------------------------------------------------
# نظام الروليت والمحقق
# -------------------------------------------------
roulette_data = {
    "players": [],
    "game_started": False,
    "killer_id": None,
    "round": 0
}

@bot.command()
async def روليت(ctx):
    if roulette_data["game_started"]:
        await ctx.send("⚠️ جولة روليت قيد التنفيذ حالياً! انتظر حتى تنتهي.")
        return
    roulette_data["players"] = []
    roulette_data["game_started"] = False
    roulette_data["killer_id"] = None
    roulette_data["round"] = 0
    await ctx.send(f"🎡 **روليت الفوضى!**\nاكتب `🔥سجل` للمشاركة (الحد الأدنى 2 لاعب).")

@bot.command()
async def سجل(ctx):
    if roulette_data["game_started"]:
        await ctx.send("⚠️ اللعبة بدأت بالفعل، لا يمكنك الانضمام الآن.")
        return
    if ctx.author in roulette_data["players"]:
        await ctx.send(f"❌ {ctx.author.mention} أنت مسجل بالفعل!")
        return
    roulette_data["players"].append(ctx.author)
    count = len(roulette_data["players"])
    await ctx.send(f"✅ {ctx.author.mention} انضم للروليت! (المشاركين الحاليين: **{count}**).")

@bot.command()
async def دور(ctx):
    if len(roulette_data["players"]) < 2:
        await ctx.send("❌ يجب أن يكون لاعبين على الأقل! اكتب `🔥سجل` أولاً.")
        return
    if roulette_data["game_started"]:
        await ctx.send("⚠️ العجلة تدور بالفعل! استخدم `🔥تحقق` للبحث عن القاتل.")
        return
    
    roulette_data["game_started"] = True
    roulette_data["round"] += 1
    
    # اختيار القاتل السري
    killer = random.choice(roulette_data["players"])
    roulette_data["killer_id"] = killer.id
    
    await ctx.send(f"🎡 **العجلة تدور...** تم اختيار قاتل سري! (الدور {roulette_data['round']})")
    await asyncio.sleep(2)
    await ctx.send("🔍 المحققون، استخدموا `🔥تحقق @الاسم` للكشف عن القاتل.")
    await ctx.send("⚔️ القاتل، استخدم `🔥اطرد @الاسم` لقتل أحد المحققين.")

@bot.command()
async def تحقق(ctx, member: discord.Member):
    if not roulette_data["game_started"]:
        await ctx.send("❌ لا توجد جولة نشطة حالياً. اكتب `🔥دور` لبدء الجولة.")
        return
    if ctx.author.id == roulette_data["killer_id"]:
        await ctx.send("❌ القاتل لا يمكنه التحقق من نفسه!")
        return
    if member.id == roulette_data["killer_id"]:
        await ctx.send(f"🕵️ **تحذير!** {member.mention} هو **القاتل!** أبلغ الجميع فوراً!")
    else:
        await ctx.send(f"✅ {member.mention} ليس القاتل. استمر في البحث.")

@bot.command()
async def اطرد(ctx, member: discord.Member):
    if not roulette_data["game_started"]:
        await ctx.send("❌ لا توجد جولة نشطة حالياً.")
        return
    if ctx.author.id != roulette_data["killer_id"]:
        await ctx.send("❌ أنت لست القاتل! القاتل فقط من يمكنه الطرد.")
        return
    if member == ctx.author:
        await ctx.send("❌ لا يمكنك طرد نفسك!")
        return
    if member not in roulette_data["players"]:
        await ctx.send("❌ هذا العضو ليس في اللعبة.")
        return
    
    # التحقق من الدرع
    data = load_data()
    mid = str(member.id)
    if mid not in data:
        data[mid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
    
    if data[mid].get("shield", 0) > 0:
        data[mid]["shield"] -= 1
        save_data(data)
        await ctx.send(f"🛡️ **{member.mention} نجا!** درعه تحطم، لكنه بقي حياً!")
    else:
        await ctx.send(f"💀 **{member.mention} تم طرده من اللعبة!** (القاتل ينتصر في هذه الجولة).")
        roulette_data["players"].remove(member)
        roulette_data["game_started"] = False
        # مكافأة للقاتل
        killer_id = str(ctx.author.id)
        if killer_id not in data:
            data[killer_id] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
        data[killer_id]["points"] += 5
        save_data(data)
        await ctx.send(f"🏆 {ctx.author.mention} ربح **5 نقاط**!")

@bot.command()
async def عشوائي(ctx):
    if not roulette_data["game_started"]:
        await ctx.send("❌ لا توجد جولة نشطة حالياً.")
        return
    if ctx.author.id != roulette_data["killer_id"]:
        await ctx.send("❌ أنت لست القاتل!")
        return
    victims = [p for p in roulette_data["players"] if p != ctx.author]
    if not victims:
        await ctx.send("❌ لا يوجد أحد لتطرده!")
        return
    victim = random.choice(victims)
    await ctx.send(f"🎲 القاتل يختار عشوائياً: {victim.mention}!")
    data = load_data()
    vid = str(victim.id)
    if vid not in data:
        data[vid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
    if data[vid].get("shield", 0) > 0:
        data[vid]["shield"] -= 1
        save_data(data)
        await ctx.send(f"🛡️ **{victim.mention} نجا!** درعه تحطم!")
    else:
        roulette_data["players"].remove(victim)
        roulette_data["game_started"] = False
        killer_id = str(ctx.author.id)
        if killer_id not in data:
            data[killer_id] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
        data[killer_id]["points"] += 5
        save_data(data)
        await ctx.send(f"💀 **{victim.mention} طُرد عشوائياً!** 🏆 {ctx.author.mention} ربح **5 نقاط**!")

# =================================================
# (7) الألعاب الترفيهية (20 لعبة)
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
    questions = ["ما هو أطول نهر في العالم؟", "كم عدد الكواكب في المجموعة الشمسية؟"]
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
async def قاتل(ctx):
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
        bot.run(TOKEN)
