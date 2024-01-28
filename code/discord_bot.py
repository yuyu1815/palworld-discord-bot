import discord
from discord import app_commands
from discord.ext import tasks
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

check_game_server=False

with open(f"./Language/{Language}", 'r', encoding='utf-8') as file:
    data = json.load(file)

with open(f"./channel_id.json", 'r', encoding='utf-8') as file:
    active_channel = json.load(file)
active_channel_id=active_channel['channel_id']
@client.event
async def on_ready():
    print("lady")
    await tree.sync()#スラッシュコマンドを同期

#help
@tree.command(name="help",description=data["help_info"])
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(data["help_list"],ephemeral=True)

#サーバーにコマンド送信
@tree.command(name="command",description=data["command"])
async def MCR_command(interaction: discord.Interaction,command: str):
    #if allowed_channel_id:
        
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
        check_game_server=True
        await interaction.response.send_message(data["log_01"],ephemeral=True)
        main.server_start()
    else:
        await interaction.response.send_message(data["Error_log_02"],ephemeral=True)

#停止コマンド
@tree.command(name="stop",description=data["stop"])
async def stop_command(interaction: discord.Interaction):
    stop=MCRcon_command.calc("stop")
    if stop :
        await interaction.response.send_message(data["stop_message"],)

    else:
        await interaction.response.send_message(data["server_error_log02"],ephemeral=True)

#update
@tree.command(name="update",description=data["update"])
async def update_command(interaction: discord.Interaction):
    if MCRcon_command.check() is False:
        try:
            subprocess.run('steamcmd +login anonymous +app_update 2394010 validate +quit')
            await interaction.response.send_message(data["update_log02"])
        except Exception as e:
            await interaction.response.send_message(data["server_error_log04"],ephemeral=True)
    else:
        await interaction.response.send_message(data["server_error_log03"],ephemeral=True)
#動いているかチェック
@tasks.loop(seconds=5)
async def send_message_(interaction):
    if not check_game_server and MCRcon_command.check():
        check_game_server=False
        await active_channel_id.send(data["stop_message"],ephemeral=True)
    player_list = MCR_command.player_status()
    for player_id in [player[1] for player in player_list]:
        player_id


#channel設定
@tree.command(name="channel",description=data["active_channel"])
async def update_command(interaction: discord.Interaction,channel_id: str):
    
    channel_id_dict={'channel':channel_id}
    with open('./channel_id.json', 'w',encoding='utf-8') as f:
        json.dump(channel_id_dict, f)

    with open(f"./channel_id.json", 'r', encoding='utf-8') as file:
        active_channel = json.load(file)
    active_channel_id=active_channel['channel']


client.run(token)

