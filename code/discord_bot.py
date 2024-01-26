import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import json
import threading

import main
import MCRcon_command
load_dotenv()
intents = discord.Intents.all()
intents.guilds = True
intents.guild_messages = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
token=os.getenv('token')
Language=os.getenv('Language')
folder_pach=os.getenv('folder_pach')

with open(f"./Language/{Language}", 'r', encoding='utf-8') as file:
    data = json.load(file)

@client.event
async def on_ready():
    print("lady")
    await tree.sync()#スラッシュコマンドを同期

@tree.command(name="help",description=data["help_info"])
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(data["help_list"],ephemeral=True)

@tree.command(name="command",description=data["command"])
async def MCR_command(interaction: discord.Interaction,command: str):
    command_log=MCRcon_command.calc(command)
    try:
        threading.Thread(target=main.server_start)
        await interaction.response.send_message(command_log,ephemeral=True)
    except Exception as e:
        print(data["Error_log_01"])

@tree.command(name="start",description=data["start"])
async def start_command(interaction: discord.Interaction):

    if folder_pach:
        await interaction.response.send_message(data["log_01"],ephemeral=True)
    else:
        await interaction.response.send_message(data["Error_log_02"],ephemeral=True)

def discord_main():
    client.run(token)