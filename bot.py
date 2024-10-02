import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os, asyncio

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

# ------- COMMANDS --------

# Help command
@bot.tree.command(name = "help", description="Lists all commands.")
async def help(interaction: discord.Interaction):
    help_message = '''\
!hello - Replies with Hello World!
!bye - Replies with Goodbye World!
!greet <name> <x> - Greets name x amount of times.
!ping - Check the bot's latency.
'''
    await interaction.response.send_message(help_message)

# Command that responds to "!hello"
@bot.tree.command(name = "hello", description="Replies with Hello World! :)")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")

# Command that responds to "!bye"
@bot.tree.command(name = "bye", description="Replies with Goodbye World!")
async def bye(interaction: discord.Interaction):
    await interaction.response.send_message("Goodbye World!")

# Command that responds to "!greet"
@bot.tree.command(name = "greet", description="Greets user.")
async def greet(interaction: discord.Interaction, name: str, times: int):
    message = f"Hello {name}!" * times
    await interaction.response.send_message(message)

# Command that measures bot's latency
@bot.tree.command(name = "ping", description="Check the bot's latency.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000) # Convert to ms
    await interaction.response.send_message(f'Pong! {latency}ms')

# Command that deletes all messages in channel
@bot.tree.command(name = "clear", description="Delete all messages in the channel.")
async def clear(interaction: discord.Interaction):
    channel = interaction.channel

    # Check if bot has permission to manage messages
    if not channel.permissions_for(interaction.user).manage_messages:
        await interaction.response.send_message("Bot does not have permission to delete messages.", ephemeral=True)
        return
    
    # Acknowledge the interaction
    await interaction.response.send_message("Deleting messages... This might take a moment.", ephemeral=True)

    # Deleting messages
    deleted_count = 0
    async for message in channel.history(limit=None):
        await message.delete()
        deleted_count += 1
        await asyncio.sleep(0.5)  # Sleep for 0.5 second to avoid rate limits

    # Followup message
    await interaction.followup.send(f"Deleted {deleted_count} messages.", ephemeral=True)

# Run the bot with your token
bot.run(TOKEN)