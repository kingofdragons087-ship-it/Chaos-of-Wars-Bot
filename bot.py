import discord
from discord.ext import commands
from discord.ui import Button, View, Select
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
# (1) القائمة التفاعلية (UI) + القصة الرئيسية
# =================================================
class MainMenuView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="⚔️ المبارزة", style=discord.ButtonStyle.danger)
    async def duel_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("لعب المبارزة: اكتب `🔥مبارزة @لاعب` لتحدي شخص.", ephemeral=True)

    @discord.ui.button(label="🎡 الروليت", style=discord.ButtonStyle.primary)
    async def roulette_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🎡 للعب الروليت: اكتب `🔥روليت`، ثم `🔥سجل`، ثم `🔥دور`.", ephemeral=True)

    @discord.ui.button(label="🛡️ المتجر", style=discord.ButtonStyle.success)
    async def shop_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🛡️ المتجر: اكتب `🔥متجر` لرؤية الأسعار.", ephemeral=True)

    @discord.ui.button(label="🎮 ألعاب ترفيهية", style=discord.ButtonStyle.secondary)
    async def games_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🎮 35+ لعبة: اكتب `🔥العاب` لرؤية القائمة الكاملة.", ephemeral=True)

    @discord.ui.button(label="💰 نقاطي", style=discord.ButtonStyle.success)
    async def points_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("💰 لمعرفة النقاط: اكتب `🔥نقاطي`.", ephemeral=True)

@bot.command()
async def قوانين(ctx):
    story = """
**⚔️ ساحة الفوضى (Chaos of Wars Arena) ⚔️**

*"في أعماق ظلام الأرض، حيث لا يصل ضوء الشمس، بنت 'النظام' ساحة موتها. أنت لست هنا بمحض إرادتك، فقد جُمعتَ من بين الملايين لتكون جزءاً من لعبة الموت... البقاء للأقوى!"*

**🔥 الأوامر الأساسية:**
• `🔥متجر` - عرض المتجر.
• `🔥نقاطي` - رصيدك الحالي.
• `🔥انضم` - التسجيل في الساحة (تحصل على 100 نقطة).
• `🔥التوب` - قائمة أفضل اللاعبين.
• `🔥كافأ @اللاعب` - للمالك والمشرفين فقط، إعطاء مكافأة.
• `🔥ID @اللاعب` - معرف المستخدم.

**⚔️ الألعاب الرئيسية:**
• `🔥مبارزة @لاعب` - تحدي 1 ضد 1.
• `🔥روليت` - بدء لعبة الروليت الجماعية.
• `🔥صندوق` - فتح صندوق جوائز (5 نقاط).
• `🔥العاب` - قائمة الألعاب الترفيهية.
    """
    embed = discord.Embed(title="🔥 قائمة الألعاب التفاعلية", description=story, color=0x1a0000)
    embed.add_field(name="📜 ابدأ مغامرتك!", value="اختر ما تريد لعبه من الأزرار أدناه.", inline=False)
    embed.set_footer(text="⚰️ الموت يضحك... وأنت تضحك معه؟")
    view = MainMenuView()
    await ctx.send(embed=embed, view=view)

# =================================================
# (2) المتجر والنقاط
# =================================================
@bot.command()
async def متجر(ctx):
    embed = discord.Embed(title="🔥 متجر الفوضى", color=0x1a0000)
    embed.add_field(name="🛡️ درع النجاة", value="3 نقاط", inline=False)
    embed.add_field(name="❄️ تجميد العجلة", value="5 نقاط", inline=False)
    embed.add_field(name="🧲 مغناطيس", value="4 نقاط", inline=False)
    embed.add_field(name="📡 رادار", value="6 نقاط", inline=False)
    embed.add_field(name="🎁 صندوق الجوائز", value="5 نقاط", inline=False)
    embed.set_footer(text="💀 الموت رخيص، لكن النقاط أثمن.")
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
        1504809491231801404,  # أنت (المالك)
        1146159441058746449,  # المشرف 1
        836777715708592129    # المشرف 2
    ]
    if uid not in data:
        if ctx.author.id in allowed_staff:
            # المشرفين والمالك يحصلون على 0 نقطة في البداية، ولكنهم يلعبون ويكتسبونها
            data[uid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
            save_data(data)
            await ctx.send(f"👑 مرحباً أيها القائد {ctx.author.mention}! رصيدك يبدأ من 0، ولكنك ستجمع النقاط وتصبح أقوى!")
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
class RewardView(View):
    def __init__(self, target_member):
        super().__init__(timeout=None)
        self.target_member = target_member

    @discord.ui.button(label="👑 رول VIP", style=discord.ButtonStyle.danger)
    async def vip_button(self, interaction: discord.Interaction, button: Button):
        # إعطاء رول VIP (سيتم إنشاؤه تلقائياً إذا لم يوجد)
        guild = interaction.guild
        vip_role = discord.utils.get(guild.roles, name="VIP")
        if vip_role is None:
            vip_role = await guild.create_role(name="VIP", color=discord.Color.gold())
        await self.target_member.add_roles(vip_role)
        await interaction.response.send_message(f"👑 {self.target_member.mention} حصل على رول **VIP**!", ephemeral=True)

    @discord.ui.button(label="🎁 صندوق عشوائي", style=discord.ButtonStyle.success)
    async def box_button(self, interaction: discord.Interaction, button: Button):
        prizes = ["10 نقاط", "درع النجاة", "تجميد العجلة", "مغناطيس", "رادار", "5 نقاط"]
        prize = random.choice(prizes)
        data = load_data()
        uid = str(self.target_member.id)
        if uid not in data:
            data[uid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
        if prize == "10 نقاط":
            data[uid]["points"] += 10
        elif prize == "5 نقاط":
            data[uid]["points"] += 5
        elif prize == "درع النجاة":
            data[uid]["shield"] += 1
        elif prize == "تجميد العجلة":
            data[uid]["freeze"] += 1
        elif prize == "مغناطيس":
            data[uid]["magnet"] += 1
        elif prize == "رادار":
            data[uid]["radar"] += 1
        save_data(data)
        await interaction.response.send_message(f"🎁 {self.target_member.mention} حصل على **{prize}** من صندوق العشوائي!", ephemeral=True)

    @discord.ui.button(label="💰 نقاط RH", style=discord.ButtonStyle.primary)
    async def points_button(self, interaction: discord.Interaction, button: Button):
        # إعطاء 50 نقطة RH
        data = load_data()
        uid = str(self.target_member.id)
        if uid not in data:
            data[uid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
        data[uid]["points"] += 50
        save_data(data)
        await interaction.response.send_message(f"💰 {self.target_member.mention} حصل على **50 نقطة RH**!", ephemeral=True)

@bot.command()
async def كافأ(ctx, member: discord.Member):
    # التحقق من أن المستخدم هو المالك أو المشرف
    allowed_users = [
        1504809491231801404,  # أنت (المالك)
        1146159441058746449,  # المشرف 1
        836777715708592129    # المشرف 2
    ]
    if ctx.author.id not in allowed_users:
        await ctx.send("⚠️ هذا الأمر للمالك والمشرفين فقط.")
        return
    
    view = RewardView(member)
    embed = discord.Embed(title="🎁 قائمة المكافآت", description=f"اختر المكافأة التي تريدها لـ {member.mention}", color=0xffd700)
    embed.add_field(name="👑 رول VIP", value="يمنح العضو رتبة VIP في السيرفر.", inline=False)
    embed.add_field(name="🎁 صندوق عشوائي", value="يمنح العضو جائزة عشوائية (نقاط، درع، تجميد...).", inline=False)
    embed.add_field(name="💰 نقاط RH", value="يمنح العضو 50 نقطة RH.", inline=False)
    await ctx.send(embed=embed, view=view)

# =================================================
# (6) أمر معرف المستخدم
# =================================================
@bot.command()
async def ID(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"🆔 معرفك: `{ctx.author.id}`")
    else:
        await ctx.send(f"🆔 معرف {member.mention}: `{member.id}`")

# =================================================
# (7) الألعاب الرئيسية (المبارزة والروليت)
# =================================================
active_duels = {}

# ردود فكاهية عند الموت
death_replies = [
    "💀 مات، بس بصراحة كان شكله ميت من زمان...",
    "⚰️ وداعاً أيها البطل... سيذكرك الجميع كـ 'الذي لم ينجح'.",
    "🎭 المسرح يخسر ممثلاً عظيماً... لكننا سنستمر!",
    "🪦 هنا يرقد... شخص كان يعتقد أنه سيخرج حياً.",
    "😵 وقع في فخ الموت... يا لها من مفاجأة!",
    "🧟 سيقوم من بين الأموات... ربما.",
    "🍿 العرض انتهى لهذا الشخص!",
    "🕯️ أطفأ شمعته... إنه ليس نجماً بعد الآن."
]

@bot.command()
async def مبارزة(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("⚠️ مثال: `🔥مبارزة @لاعب`")
        return
    if member == ctx.author:
        await ctx.send("❌ لا يمكنك مبارزة نفسك!")
        return
    if ctx.author.id in active_duels:
        await ctx.send("⚠️ أنت مشغول بمبارزة حالياً.")
        return
    for duel in active_duels.values():
        if duel["opponent"] == member.id or duel["challenger"] == member.id:
            await ctx.send(f"❌ {member.mention} مشغول بمبارزة حالياً.")
            return
    active_duels[ctx.author.id] = {
        "challenger": ctx.author.id,
        "opponent": member.id,
        "accepted": False
    }
    await ctx.send(f"⚔️ {ctx.author.mention} يتحدى {member.mention}!\nاكتب `🔥قبول` لقبول التحدي.")

@bot.command()
async def قبول(ctx):
    challenger_id = None
    for cid, duel in active_duels.items():
        if duel["opponent"] == ctx.author.id:
            challenger_id = cid
            break
    if challenger_id is None:
        await ctx.send("❌ لا يوجد تحدي لك حالياً.")
        return
    challenger = bot.get_user(challenger_id)
    winner = random.choice([challenger, ctx.author])
    await ctx.send(f"⚔️ المبارزة بدأت بين {challenger.mention} و {ctx.author.mention}!")
    await asyncio.sleep(2)
    await ctx.send(f"🏆 الفائز هو **{winner.mention}**! (+2 نقطة)")
    loser = ctx.author if winner == challenger else challenger
    await ctx.send(f"💀 **{loser.mention}** {random.choice(death_replies)}")
    w_uid = str(winner.id)
    db = load_data()
    if w_uid not in db:
        db[w_uid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
    db[w_uid]["points"] += 2
    save_data(db)
    del active_duels[challenger_id]

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
    data = load_data()
    mid = str(member.id)
    if mid not in data:
        data[mid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
    if data[mid].get("shield", 0) > 0:
        data[mid]["shield"] -= 1
        save_data(data)
        await ctx.send(f"🛡️ **{member.mention} نجا!** درعه تحطم، لكنه بقي حياً!")
    else:
        await ctx.send(f"💀 **{member.mention}** {random.choice(death_replies)}")
        roulette_data["players"].remove(member)
        roulette_data["game_started"] = False
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
        await ctx.send(f"💀 **{victim.mention}** {random.choice(death_replies)}")
        roulette_data["players"].remove(victim)
        roulette_data["game_started"] = False
        killer_id = str(ctx.author.id)
        if killer_id not in data:
            data[killer_id] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
        data[killer_id]["points"] += 5
        save_data(data)
        await ctx.send(f"🏆 {ctx.author.mention} ربح **5 نقاط**!")

# =================================================
# (8) الألعاب الترفيهية (35+ لعبة)
# =================================================
@bot.command()
async def العاب(ctx):
    embed = discord.Embed(title="🎮 35 لعبة مسلية في البوت!", description="استمتع بمجموعة متنوعة من الألعاب", color=0x00ff00)
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
    embed.add_field(name="💡 لغز", value="`🔥لغز`", inline=False)
    embed.add_field(name="🎭 تمثيل", value="`🔥تمثيل`", inline=False)
    embed.add_field(name="🧠 عقل", value="`🔥عقل`", inline=False)
    embed.add_field(name="📖 حكمة", value="`🔥حكمة`", inline=False)
    embed.add_field(name="🦸 بطل", value="`🔥بطل`", inline=False)
    embed.add_field(name="👽 فضائي", value="`🔥فضائي`", inline=False)
    embed.add_field(name="🦄 سحري", value="`🔥سحري`", inline=False)
    embed.add_field(name="🎪 سيرك", value="`🔥سيرك`", inline=False)
    embed.add_field(name="⚡ برق", value="`🔥برق`", inline=False)
    embed.add_field(name="🌊 بحر", value="`🔥بحر`", inline=False)
    embed.add_field(name="🏔️ جبل", value="`🔥جبل`", inline=False)
    embed.add_field(name="🌌 فضاء", value="`🔥فضاء`", inline=False)
    embed.add_field(name="🕰️ زمن", value="`🔥زمن`", inline=False)
    embed.add_field(name="🎯 هدف", value="`🔥هدف`", inline=False)
    embed.add_field(name="🧩 أحجية", value="`🔥أحجية`", inline=False)
    await ctx.send(embed=embed)

# -------------------------------------------------
# نظام الألعاب التفاعلية (التي تطلب إجابة)
# -------------------------------------------------
# قاموس لتخزين جلسات اللاعبين
game_sessions = {}

@bot.command()
async def لغز(ctx):
    user_id = ctx.author.id
    riddles = [
        {"q": "ما هو الشيء الذي يكسره الكلام؟", "a": "الصمت"},
        {"q": "ما هو الشيء الذي كلما زاد نقص؟", "a": "العمر"},
        {"q": "ما هو الباب الذي لا يمكن فتحه؟", "a": "باب الأمل"},
        {"q": "ما هو الشيء الذي يملك قلباً لكنه لا ينبض؟", "a": "الخس"},
        {"q": "ما هو الشيء الذي يسير بلا أرجل؟", "a": "الزمن"},
    ]
    chosen = random.choice(riddles)
    game_sessions[user_id] = {"type": "لغز", "question": chosen["q"], "answer": chosen["a"], "attempts": 0, "max_attempts": 3, "answered": False}
    await ctx.send(f"🧩 **لغز:** {chosen['q']}\nلديك 3 محاولات. اكتب الإجابة.")

@bot.command()
async def سؤال(ctx):
    user_id = ctx.author.id
    questions = [
        {"q": "ما هو أطول نهر في العالم؟", "a": "النيل"},
        {"q": "كم عدد الكواكب في المجموعة الشمسية؟", "a": "8"},
        {"q": "ما هي عاصمة مصر؟", "a": "القاهرة"},
    ]
    chosen = random.choice(questions)
    game_sessions[user_id] = {"type": "سؤال", "question": chosen["q"], "answer": chosen["a"], "attempts": 0, "max_attempts": 2, "answered": False}
    await ctx.send(f"❓ **سؤال:** {chosen['q']}\nلديك محاولتان. اكتب الإجابة.")

@bot.command()
async def تخمين(ctx):
    user_id = ctx.author.id
    number = random.randint(1, 10)
    game_sessions[user_id] = {"type": "تخمين", "question": "خمن الرقم من 1 إلى 10", "answer": str(number), "attempts": 0, "max_attempts": 3, "answered": False}
    await ctx.send(f"🔢 **خمن الرقم:** 1 إلى 10\nلديك 3 محاولات. اكتب رقمك.")

@bot.command()
async def إجابة(ctx, *, answer: str = None):
    user_id = ctx.author.id
    if user_id not in game_sessions:
        await ctx.send("❌ أنت لا تشارك في أي لعبة حالياً. ابدأ لعبة أولاً.")
        return
    session = game_sessions[user_id]
    if session["answered"]:
        await ctx.send("✅ لقد أجبت مسبقاً. ابدأ لعبة جديدة.")
        return
    if answer is None:
        await ctx.send("⚠️ اكتب إجابتك: `🔥إجابة إجابتك`")
        return
    correct = session["answer"]
    if answer.strip().lower() == correct.lower():
        session["answered"] = True
        await ctx.send(f"🎉 **إجابة صحيحة!** الجواب هو **{correct}**\nلقد ربحت **3 نقاط**!")
        data = load_data()
        uid = str(user_id)
        if uid not in data:
            data[uid] = {"points": 0, "shield": 0, "freeze": 0, "magnet": 0, "radar": 0}
        data[uid]["points"] += 3
        save_data(data)
        del game_sessions[user_id]
    else:
        session["attempts"] += 1
        remaining = session["max_attempts"] - session["attempts"]
        if session["attempts"] >= session["max_attempts"]:
            await ctx.send(f"❌ لقد استنفذت محاولاتك! الإجابة الصحيحة: **{correct}**")
            del game_sessions[user_id]
        else:
            await ctx.send(f"❌ خطأ! تبقى **{remaining}** محاولة.")

# -------------------------------------------------
# الألعاب الباقية (بدون إجابة)
# -------------------------------------------------
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
    fates = ["أنت مكتوب لك النصر.", "قدرك غامض... احذر.", "النجوم تقول إنك ستنجح."]
    await ctx.send(f"🌀 {random.choice(fates)}")

@bot.command()
async def طالع(ctx):
    signs = ["الحمل", "الثور", "الجوزاء", "السرطان", "الأسد", "العذراء", "الميزان", "العقرب", "القوس", "الجدي", "الدلو", "الحوت"]
    await ctx.send(f"🌟 طالعك: **{random.choice(signs)}**")

@bot.command()
async def لون(ctx):
    colors = ["أحمر", "أزرق", "أخضر", "أصفر", "أبيض", "أسود", "بنفسجي", "برتقالي", "وردي"]
    await ctx.send(f"🎨 لونك: **{random.choice(colors)}**")

@bot.command()
async def حيوان(ctx):
    animals = ["أسد", "نمر", "فيل", "زرافة", "دلفين", "صقر", "ثعبان", "حوت", "نسر", "ذئب", "أرنب"]
    await ctx.send(f"🐾 حيوانك: **{random.choice(animals)}**")

@bot.command()
async def غذاء(ctx):
    foods = ["بيتزا", "برغر", "سوشي", "شاورما", "معكرونة", "دجاج مشوي", "سلطة", "شوربة", "سمك", "كباب"]
    await ctx.send(f"🍔 الغذاء: **{random.choice(foods)}**")

@bot.command()
async def حظ(ctx):
    await ctx.send(f"🍀 حظك: **{random.randint(0, 100)}%**")

@bot.command()
async def رحلة(ctx):
    destinations = ["باريس", "طوكيو", "نيويورك", "لندن", "دبي", "القاهرة", "اسطنبول", "روما", "برلين", "مدريد"]
    await ctx.send(f"✈️ وجهتك: **{random.choice(destinations)}**")

@bot.command()
async def تمثيل(ctx):
    actions = ["مهرج", "شخصية تاريخية", "حيوان", "بطل خارق", "شرير"]
    await ctx.send(f"🎭 دورك اليوم: **{random.choice(actions)}**")

@bot.command()
async def عقل(ctx):
    mind_quotes = ["العقل السليم في الجسم السليم.", "الفكر هو سلاح الأقوياء.", "تعلم من الأمس، عش اليوم، وخطط للغد."]
    await ctx.send(f"🧠 {random.choice(mind_quotes)}")

@bot.command()
async def حكمة(ctx):
    wisdom = ["الصبر مفتاح الفرج.", "من جد وجد، ومن زرع حصد.", "السكوت علامة الرضا.", "العلم نور والجهل ظلام.", "الأخلاق هي زينة الإنسان."]
    await ctx.send(f"📖 **{random.choice(wisdom)}**")

@bot.command()
async def بطل(ctx):
    heros = ["أنت الفارس الذي سيحرر المملكة!", "البطل الحقيقي هو من يقف بجانب المحتاج.", "قوتك تكمن في قلبك."]
    await ctx.send(f"🦸 {random.choice(heros)}")

@bot.command()
async def فضائي(ctx):
    aliens = ["الكائنات الفضائية تراقبك الآن...", "هل سمعت عن حضارة المريخ القديمة؟", "هناك حياة في كوكب آخر."]
    await ctx.send(f"👽 {random.choice(aliens)}")

@bot.command()
async def سحري(ctx):
    magical = ["السحر يكمن في عينيك.", "أنت مميز، لا تنسَ ذلك.", "الكون يرسل لك رسالة."]
    await ctx.send(f"🦄 {random.choice(magical)}")

@bot.command()
async def سيرك(ctx):
    circus = ["مرحباً بك في سيرك العجائب!", "شاهد المهرجين وهم يؤدون عروضهم.", "السيرك هو مكان الخيال."]
    await ctx.send(f"🎪 {random.choice(circus)}")

@bot.command()
async def برق(ctx):
    lightning = ["البرق يضرب، والعاصفة تقترب.", "الرعد قادم... استعد.", "البرق ينير السماء الحالكة."]
    await ctx.send(f"⚡ {random.choice(lightning)}")

@bot.command()
async def بحر(ctx):
    sea = ["البحر يحمل أسراراً كثيرة.", "الأمواج تتحدث بلغة هادئة.", "غروب الشمس على البحر هو الأجمل."]
    await ctx.send(f"🌊 {random.choice(sea)}")

@bot.command()
async def جبل(ctx):
    mountain = ["الجبال شاهقة وقوية.", "القمة هي وجهتك التالية.", "في الجبال يجد الإنسان نفسه."]
    await ctx.send(f"🏔️ {random.choice(mountain)}")

@bot.command()
async def فضاء(ctx):
    space = ["الفضاء لا نهاية له.", "النجوم تهمس بأسرار الكون.", "هل نحن وحدنا في هذا الكون؟"]
    await ctx.send(f"🌌 {random.choice(space)}")

@bot.command()
async def هدف(ctx):
    goals = ["ركز على هدفك وستصل إليه.", "لا تستسلم أبداً.", "كل خطوة تقربك إلى النجاح."]
    await ctx.send(f"🎯 {random.choice(goals)}")

# =================================================
# (9) تشغيل البوت
# =================================================
if __name__ == "__main__":
    if TOKEN is None:
        print("❌ التوكن مفقود!")
    else:
        bot.run(TOKEN)
