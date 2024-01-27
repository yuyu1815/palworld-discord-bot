import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import json
import threading
import subprocess

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
#サーバーにコマンド送信
@tree.command(name="command",description=data["command"])
async def MCR_command(interaction: discord.Interaction,command: str):
    if not command == command.find('Shutdown') or command == command.find('DoExit'):
        command_log=MCRcon_command.calc(command)
        try:
            threading.Thread(target=main.server_start)
            await interaction.response.send_message(command_log,ephemeral=True)
        except Exception as e:
            print(data["Error_log_01"])
    else:
        await interaction.response.send_message(data["log_02"],ephemeral=True)

#開始コマンド
@tree.command(name="start",description=data["start"])
async def start_command(interaction: discord.Interaction):

    if folder_pach:
        await interaction.response.send_message(data["log_01"],ephemeral=True)
    else:
        await interaction.response.send_message(data["Error_log_02"],ephemeral=True)

#停止コマンド
@tree.command(name="stop",description=data["stop"])
async def stop_command(interaction: discord.Interaction):
    stop=MCRcon_command.calc("stop")
    if stop :
        await interaction.response.send_message(data["stop_message"],ephemeral=True)
    else:
        await interaction.response.send_message(data["server_error_log02"],ephemeral=True)
#update
@tree.command(name="update",description=data["update"])
async def update_command(interaction: discord.Interaction):
    if(MCRcon_command.check() is False):
        await interaction.response.send_message(data["update_log01"],ephemeral=True)
        subprocess.run(['steamcmd +login anonymous +app_update 2394010 validate +quit'])
        await interaction.response.send_message(data["update_log02"],ephemeral=True)
    else:
        await interaction.response.send_message(data["update_log03"],ephemeral=True)




def discord_main():
    client.run(token)