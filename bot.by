import discord
from discord.ext import commands
import json
import os
import random
import asyncio

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
        await ctx.send("⚠️ يجب إكمال البيانات. مثال: `🔥مبارزة @لاعب`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("⚠️ العضو غير موجود. تأكد من الاسم مع @")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("⚠️ هذا الأمر للمالك والمشرفين فقط.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send("⚠️ حدث خطأ. حاول مرة أخرى.")

# =================================================
# (1) القصة والبوابة
# =================================================
@bot.command()
async def قوانين(ctx):
    story = """
**📜 ساحة الفوضى (Chaos of Wars Arena) 📜**

في عالمٍ لم يعد يعرف معنى العدالة، ظهرت منظمة غامضة تُدعى "النظام".
قررت هذه المنظمة بناء أعظم ساحة قتال تحت الأرض على الإطلاق.
أنت لست هنا بمحض إرادتك. لقد تم اختطافك، وتستيقظ لتجد نفسك داخل غرفة زجاجية معتمة.

*"مرحباً أيها المختار. القاعدة الوحيدة هنا هي: البقاء على قيد الحياة."*

**🔥 الأوامر الأساسية:**
• `🔥متجر` - عرض المتجر.
• `🔥نقاطي` - رصيدك الحالي.
• `🔥انضم` - التسجيل في الساحة (تحصل على 100 نقطة).
• `🔥التوب` - قائمة أفضل اللاعبين.
• `🔥كافأ @اللاعب عدد` - للمالك والمشرفين فقط، إعطاء نقاط.

**⚔️ الألعاب الرئيسية:**
• `🔥مبارزة @لاعب` - تحدي 1 ضد 1.
• `🔥روليت` - بدء لعبة الروليت الجماعية.
• `🔥صندوق` - فتح صندوق جوائز (5 نقاط).
    """
    await ctx.send(story)

# =================================================
# (2) المتجر والنقاط
# =================================================
@bot.command()
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
