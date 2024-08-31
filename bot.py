import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Set up the bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event that triggers when the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

    # Print registered commands
    for command in bot.tree.get_commands():
        print(f'Registered command: {command.name}')


# Command that respond to "!hello"
@bot.tree.command(name = "hello", description="Replies with Hello World! :)")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")

@bot.tree.command(name = "bye", description="Replies with Goodbye World!")
async def bye(interaction: discord.Interaction):
    await interaction.response.send_message("Goodbye World!")

# Run the bot with your token
bot.run(TOKEN)