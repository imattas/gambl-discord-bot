import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio, random, sqlite3, datetime

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)
TREE = bot.tree

db = sqlite3.connect("economy.db")
cursor = db.cursor()

# --- DB Setup ---
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    wallet INTEGER DEFAULT 1000,
    bank INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
    user_id INTEGER,
    item TEXT,
    PRIMARY KEY (user_id, item)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS shop (
    item TEXT PRIMARY KEY,
    price INTEGER
)''')

heist_participants = []

# --- Helper Functions ---

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        db.commit()
        return (user_id, 1000, 0, 0, 1)
    return user

def update_user(user_id, column, amount):
    get_user(user_id)
    cursor.execute(f"UPDATE users SET {column} = {column} + ? WHERE user_id = ?", (amount, user_id))
    db.commit()

def set_user(user_id, column, amount):
    get_user(user_id)
    cursor.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (amount, user_id))
    db.commit()

def level_up(user_id):
    cursor.execute("SELECT xp, level FROM users WHERE user_id = ?", (user_id,))
    xp, level = cursor.fetchone()
    required = 100 * level
    if xp >= required:
        set_user(user_id, "xp", xp - required)
        set_user(user_id, "level", level + 1)
        return level + 1
    return None

# --- Economy Commands ---

@TREE.command(name="balance", description="Check your balance")
async def balance(interaction: discord.Interaction):
    _, wallet, bank, *_ = get_user(interaction.user.id)
    embed = discord.Embed(title=f"{interaction.user.name}'s Balance", color=discord.Color.green())
    embed.add_field(name="Wallet", value=f"{wallet} 🪙")
    embed.add_field(name="Bank", value=f"{bank} 🏦")
    await interaction.response.send_message(embed=embed)

@TREE.command(name="daily", description="Claim daily coins")
async def daily(interaction: discord.Interaction):
    update_user(interaction.user.id, "wallet", 500)
    await interaction.response.send_message("You claimed 500 🪙 for your daily bonus!")

@TREE.command(name="work", description="Work to earn coins")
async def work(interaction: discord.Interaction):
    amount = random.randint(100, 300)
    update_user(interaction.user.id, "wallet", amount)
    update_user(interaction.user.id, "xp", 20)
    new_level = level_up(interaction.user.id)
    msg = f"You worked and earned {amount} 🪙!"
    if new_level:
        msg += f"\n🎉 You leveled up to level {new_level}!"
    await interaction.response.send_message(msg)

@TREE.command(name="deposit", description="Deposit coins to your bank")
@app_commands.describe(amount="Amount to deposit")
async def deposit(interaction: discord.Interaction, amount: int):
    _, wallet, *_ = get_user(interaction.user.id)
    if wallet >= amount:
        update_user(interaction.user.id, "wallet", -amount)
        update_user(interaction.user.id, "bank", amount)
        await interaction.response.send_message(f"Deposited {amount} 🪙 to your bank.")
    else:
        await interaction.response.send_message("You don't have enough in your wallet.", ephemeral=True)

@TREE.command(name="withdraw", description="Withdraw coins from your bank")
@app_commands.describe(amount="Amount to withdraw")
async def withdraw(interaction: discord.Interaction, amount: int):
    _, _, bank, *_ = get_user(interaction.user.id)
    if bank >= amount:
        update_user(interaction.user.id, "bank", -amount)
        update_user(interaction.user.id, "wallet", amount)
        await interaction.response.send_message(f"Withdrew {amount} 🪙 from your bank.")
    else:
        await interaction.response.send_message("You don't have enough in your bank.", ephemeral=True)

# --- Gambling ---

@TREE.command(name="coinflip", description="Heads or tails for coins")
@app_commands.describe(side="heads or tails", amount="Amount to bet")
async def coinflip(interaction: discord.Interaction, side: str, amount: int):
    side = side.lower()
    if side not in ["heads", "tails"]:
        return await interaction.response.send_message("Pick heads or tails!", ephemeral=True)
    _, wallet, *_ = get_user(interaction.user.id)
    if wallet < amount:
        return await interaction.response.send_message("Not enough coins.", ephemeral=True)
    result = random.choice(["heads", "tails"])
    if result == side:
        update_user(interaction.user.id, "wallet", amount)
        msg = f"It's {result}! You won {amount} 🪙"
    else:
        update_user(interaction.user.id, "wallet", -amount)
        msg = f"It's {result}! You lost {amount} 🪙"
    await interaction.response.send_message(msg)

@TREE.command(name="roulette", description="Bet on red, black, or green")
@app_commands.describe(color="red, black, green", amount="Amount to bet")
async def roulette(interaction: discord.Interaction, color: str, amount: int):
    color = color.lower()
    if color not in ["red", "black", "green"]:
        return await interaction.response.send_message("Pick red, black, or green.", ephemeral=True)
    _, wallet, *_ = get_user(interaction.user.id)
    if wallet < amount:
        return await interaction.response.send_message("Not enough coins.", ephemeral=True)
    result = random.choices(["red", "black", "green"], weights=[48, 48, 4])[0]
    if result == color:
        multiplier = 2 if color != "green" else 14
        win = amount * multiplier
        update_user(interaction.user.id, "wallet", win)
        await interaction.response.send_message(f"🎯 It's {result}! You won {win} 🪙")
    else:
        update_user(interaction.user.id, "wallet", -amount)
        await interaction.response.send_message(f"💀 It's {result}. You lost {amount} 🪙")

@TREE.command(name="slots", description="Spin the slot machine")
@app_commands.describe(amount="Amount to bet")
async def slots(interaction: discord.Interaction, amount: int):
    _, wallet, *_ = get_user(interaction.user.id)
    if wallet < amount:
        return await interaction.response.send_message("Not enough coins.", ephemeral=True)
    symbols = ["🍒", "🍋", "💎", "🔔"]
    roll = [random.choice(symbols) for _ in range(3)]
    update_user(interaction.user.id, "wallet", -amount)
    win = 0
    if roll[0] == roll[1] == roll[2]:
        win = amount * 5
    elif roll.count(roll[0]) == 2 or roll.count(roll[1]) == 2:
        win = amount * 2
    if win:
        update_user(interaction.user.id, "wallet", win)
    await interaction.response.send_message(f"🎰 {' | '.join(roll)}\nYou {'won' if win else 'lost'} {win or amount} 🪙")

@TREE.command(name="rob", description="Rob another user")
@app_commands.describe(target="User to rob")
async def rob(interaction: discord.Interaction, target: discord.Member):
    if target.id == interaction.user.id:
        return await interaction.response.send_message("You can't rob yourself!", ephemeral=True)
    thief = get_user(interaction.user.id)
    victim = get_user(target.id)
    if victim[1] < 100:
        return await interaction.response.send_message("Target has too little to rob.", ephemeral=True)
    amount = random.randint(50, min(500, victim[1]))
    caught = random.random() < 0.4
    if caught:
        fine = amount
        update_user(interaction.user.id, "wallet", -fine)
        await interaction.response.send_message(f"🚓 You were caught and fined {fine} 🪙")
    else:
        update_user(interaction.user.id, "wallet", amount)
        update_user(target.id, "wallet", -amount)
        await interaction.response.send_message(f"💰 You stole {amount} 🪙 from {target.name}")

# --- Heist System ---
@TREE.command(name="heist", description="Join a group heist")
async def heist(interaction: discord.Interaction):
    if interaction.user.id in heist_participants:
        return await interaction.response.send_message("You're already in the heist queue.")
    heist_participants.append(interaction.user.id)
    await interaction.response.send_message("You joined the heist. Waiting for 3+ users...")

    await asyncio.sleep(10)
    if len(heist_participants) >= 3:
        success = random.random() < 0.7
        total_loot = random.randint(1000, 3000)
        per_user = total_loot // len(heist_participants)
        result = f"💣 Heist {'succeeded' if success else 'failed'}!\n"
        for uid in heist_participants:
            if success:
                update_user(uid, "wallet", per_user)
                result += f"<@{uid}> gained {per_user} 🪙\n"
            else:
                loss = 200
                update_user(uid, "wallet", -loss)
                result += f"<@{uid}> lost {loss} 🪙\n"
        heist_participants.clear()
        await interaction.channel.send(result)

# --- Shop System ---
@TREE.command(name="shop", description="View items for sale")
async def shop(interaction: discord.Interaction):
    cursor.execute("SELECT * FROM shop")
    items = cursor.fetchall()
    embed = discord.Embed(title="🛍️ Shop")
    for name, price in items:
        embed.add_field(name=name, value=f"{price} 🪙", inline=False)
    await interaction.response.send_message(embed=embed)

@TREE.command(name="buy", description="Buy item from shop")
@app_commands.describe(item="Item name to buy")
async def buy(interaction: discord.Interaction, item: str):
    cursor.execute("SELECT price FROM shop WHERE item = ?", (item,))
    result = cursor.fetchone()
    if not result:
        return await interaction.response.send_message("Item not found.", ephemeral=True)
    price = result[0]
    _, wallet, *_ = get_user(interaction.user.id)
    if wallet < price:
        return await interaction.response.send_message("Not enough coins.", ephemeral=True)
    update_user(interaction.user.id, "wallet", -price)
    cursor.execute("INSERT OR REPLACE INTO inventory (user_id, item) VALUES (?, ?)", (interaction.user.id, item))
    db.commit()
    await interaction.response.send_message(f"You bought {item} for {price} 🪙")

@TREE.command(name="inventory", description="Check your items")
async def inventory(interaction: discord.Interaction):
    cursor.execute("SELECT item FROM inventory WHERE user_id = ?", (interaction.user.id,))
    items = [row[0] for row in cursor.fetchall()]
    await interaction.response.send_message("🎒 Your items:\n" + ", ".join(items) if items else "You own nothing.")

# --- XP + Leaderboard ---
@TREE.command(name="rank", description="Check your level")
async def rank(interaction: discord.Interaction):
    _, _, _, xp, level = get_user(interaction.user.id)
    await interaction.response.send_message(f"📊 Level {level} | XP: {xp}/ {100 * level}")

@TREE.command(name="leaderboard", description="Top 10 richest users")
async def leaderboard(interaction: discord.Interaction):
    cursor.execute("SELECT user_id, wallet FROM users ORDER BY wallet DESC LIMIT 10")
    rows = cursor.fetchall()
    desc = "\n".join([f"<@{uid}> - {amt} 🪙" for uid, amt in rows])
    await interaction.response.send_message(embed=discord.Embed(title="💸 Leaderboard", description=desc))

# --- Admin Commands ---
@TREE.command(name="give", description="[Admin] Give coins")
@app_commands.describe(user="Target", amount="Amount")
async def give(interaction: discord.Interaction, user: discord.Member, amount: int):
    if not any(role.id == 1394342360158306325 for role in interaction.user.roles):
        return await interaction.response.send_message("Admin only.", ephemeral=True)
    update_user(user.id, "wallet", amount)
    await interaction.response.send_message(f"Gave {amount} 🪙 to {user.mention}")

@TREE.command(name="setshop", description="[Admin] Add shop item")
@app_commands.describe(item="Item name", price="Price in coins")
async def setshop(interaction: discord.Interaction, item: str, price: int):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Admin only.", ephemeral=True)
    cursor.execute("INSERT OR REPLACE INTO shop (item, price) VALUES (?, ?)", (item, price))
    db.commit()
    await interaction.response.send_message(f"Added {item} to the shop for {price} 🪙")

# --- Giveaway System ---

giveaway_entries = {}

@TREE.command(name="giveaway", description="Start a giveaway (role-restricted)")
@app_commands.describe(prize="Prize name", duration="Duration in seconds")
async def giveaway(interaction: discord.Interaction, prize: str, duration: int):
    allowed_role_id = 1394337905387897054
    if not any(role.id == allowed_role_id for role in interaction.user.roles):
        return await interaction.response.send_message("❌ You don't have permission to start giveaways.", ephemeral=True)

    embed = discord.Embed(
        title="🎉 Giveaway Started!",
        description=f"Prize: **{prize}**\nDuration: {duration} seconds\nClick below to enter!",
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Started by {interaction.user}")

    class JoinButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label="🎉 Enter Giveaway", style=discord.ButtonStyle.green)

        async def callback(self, button_interaction: discord.Interaction):
            message_id = button_interaction.message.id
            user_id = button_interaction.user.id
            if message_id not in giveaway_entries:
                giveaway_entries[message_id] = set()
            giveaway_entries[message_id].add(user_id)
            await button_interaction.response.send_message("✅ You've entered the giveaway!", ephemeral=True)

    view = discord.ui.View()
    view.add_item(JoinButton())

    await interaction.response.send_message(embed=embed, view=view)
    giveaway_message = await interaction.original_response()

    await asyncio.sleep(duration)

    entries = giveaway_entries.get(giveaway_message.id, set())
    if not entries:
        await giveaway_message.edit(embed=discord.Embed(title="🎉 Giveaway Ended", description="No entries. Giveaway cancelled.", color=discord.Color.red()), view=None)
        return

    winner_id = random.choice(list(entries))
    winner_mention = f"<@{winner_id}>"
    end_embed = discord.Embed(
        title="🎉 Giveaway Ended!",
        description=f"The winner of **{prize}** is {winner_mention}! Congratulations! 🎊",
        color=discord.Color.green()
    )
    await giveaway_message.edit(embed=end_embed, view=None)

    giveaway_entries.pop(giveaway_message.id, None)

# --- Welcomer ---

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1394331213204033789)
    if channel:
        embed = discord.Embed(
            title="👋 Welcome!",
            description=f"Welcome to **{member.guild.name}**, {member.mention}!",
            color=discord.Color.blue()
        )
        if member.guild.icon:
            embed.set_thumbnail(url=member.guild.icon.url)
        await channel.send(embed=embed)

# --- Bot Start ---

@bot.event
async def on_ready():
    await TREE.sync()

    # Bulk add shop items if missing
    items_to_add = [
        ("Bronze Medal", 100),
        ("Silver Medal", 500),
        ("Worker Gloves", 1_000),
        ("Wooden Shield", 5_000),
        ("Iron Sword", 10_000),
        ("Steel Armor", 50_000),
        ("Golden Car", 100_000),
        ("Space Helmet", 500_000),
        ("Laser Rifle", 1_000_000),
        ("Plasma Tank", 5_000_000),
        ("Alien Pet", 10_000_000),
        ("Moon Lander", 25_000_000),
        ("Private Island", 50_000_000),
        ("Time Machine", 100_000_000)
    ]

    for item, price in items_to_add:
        cursor.execute("INSERT OR IGNORE INTO shop (item, price) VALUES (?, ?)", (item, price))
    db.commit()

    print(f"Bot online as {bot.user}")

bot.run("YOUR_BOT_API")
