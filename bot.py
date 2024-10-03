import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from botHelper import *
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
    if not channel.permissions_for(interaction.user).manage_messages:
        await interaction.response.send_message("Bot does not have permission to delete messages.", ephemeral=True)
        return
       
    await interaction.response.send_message("Deleting messages... This might take a moment.", ephemeral=True)

    deleted_count = 0
    async for message in channel.history(limit=None):
        await message.delete()
        deleted_count += 1
        await asyncio.sleep(0.5) 
    await channel.send(f"Deleted {deleted_count} messages.")

# Command that allows user to archive
@bot.tree.command(name="archive", description="Archives messages and creates a command to access.")
async def archive(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Please type your messages to archive as '{name}'. Type 'done' when you're finished.")
    
    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    messages = []  # List to store the messages

    try:
        while True:
            archived_message = await bot.wait_for('message', check=check, timeout=60)  # Wait for a message

            # Check if the user is done
            if archived_message.content.lower() == 'done':
                break

            # Save the message content
            messages.append(archived_message)

    except asyncio.TimeoutError:
        await interaction.followup.send("You took too long to respond. Please try the command again.")
        return

    # Prepare to send the archived messages
    msg_format = ""
    for msg in messages:
        if msg.attachments:
            if msg_format:
                await send_in_chunks(interaction, msg_format)
                msg_format = ""

            for attachment in msg.attachments:
                await interaction.channel.send(attachment.url)  # Send each attachment individually
        else:
            msg_format += "\n" + msg.content  # Accumulate regular text messages

    # Send any remaining text messages
    if msg_format:
        await send_in_chunks(interaction, msg_format)

# Run the bot with your token
bot.run(TOKEN)