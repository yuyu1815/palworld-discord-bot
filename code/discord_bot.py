import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv
import os
import json
import threading
import subprocess
import asyncio

import main
import MCRcon_command
import steam_search

load_dotenv()
intents = discord.Intents.all()
intents.guilds = True
intents.guild_messages = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

token=os.getenv('token')
Language=os.getenv('Language')
folder_pach=os.getenv('folder_pach')

check_game_server = False
old_player_ids = []
new_player_ids = []
with open(f"./Language/{Language}", 'r', encoding='utf-8') as file:
    data = json.load(file)

with open(f"./channel_id.json", 'r', encoding='utf-8') as file:
    active_channel_json = json.load(file)
if active_channel_json['channel']:
    active_channel_id=active_channel_json['channel']
    active_channel = client.get_channel(int(active_channel_id))

@client.event
async def on_ready():
    print("discord bot lady")
    await tree.sync()#スラッシュコマンドを同期
    loop.start()
    check_game_server=False

#help
@tree.command(name="help",description=data["help_info"])
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(data["help_list"],ephemeral=True)

#サーバーにコマンド送信
@tree.command(name="command",description=data["command"])
async def MCR_command(interaction: discord.Interaction,command: str):
    #if allowed_channel_id:
        
    if not command == command.find('Shutdown') or command == command.find('DoExit') or command ==  command.find('kick') or command == command.find('ban'):
        command_log=MCRcon_command.calc(command)
        try:
            game_server_start=threading.Thread(target=main.server_start)
            game_server_start.start()
            await interaction.response.send_message(command_log,ephemeral=True)
        except Exception as e:
            print(data["Error_log_01"])
            await interaction.response.send_message(data["Error_log_01"])
    else:
        await interaction.response.send_message(data["log_02"],ephemeral=True)

#開始コマンド
@tree.command(name="start",description=data["start"])
async def start_command(interaction: discord.Interaction):

    if folder_pach:
        check_game_server=True
        await interaction.response.send_message(data["log_01"])
        game_server_start=threading.Thread(target=main.server_start)
        game_server_start.start()
    else:
        await interaction.response.send_message(data["Error_log_02"],ephemeral=True)

#停止コマンド
@tree.command(name="stop",description=data["stop"])
async def stop_command(interaction: discord.Interaction):
    if MCRcon_command.check():
        shutdown_message=data['shutdown_message']
        stop=MCRcon_command.calc(f'Shutdown 30 {shutdown_message}')
        if stop :
            await interaction.response.send_message(data["stop_message"])

        else:
            await interaction.response.send_message(data["server_error_log02"],ephemeral=True)
    else:
        await interaction.response.send_message(data["server_error_log01"])
#Restart
@tree.command(name="restart",description=data["restart"])
async def update_command(interaction: discord.Interaction):
    await interaction.response.send_message(data["log_04"])
    main.server_restart()
    

#update
@tree.command(name="update",description=data["update"])
async def update_command(interaction: discord.Interaction):
    if MCRcon_command.check():
        try:
            subprocess.run('steamcmd +login anonymous +app_update 2394010 validate +quit')
            await interaction.response.send_message(data["update_log02"])
        except Exception as e:
            await interaction.response.send_message(data["server_error_log04"],ephemeral=True)
    else:
        await interaction.response.send_message(data["server_error_log03"],ephemeral=True)

#channel設定
@tree.command(name="channel",description=data["active_channel"])
async def update_command(interaction: discord.Interaction,channel_id: str):
    
    channel_id_dict={'channel':channel_id}
    with open('./channel_id.json', 'w',encoding='utf-8') as f:
        json.dump(channel_id_dict, f)

    with open(f"./channel_id.json", 'r', encoding='utf-8') as file:
        active_channel_json = json.load(file)
    active_channel_id=active_channel_json['channel']
    await interaction.response.send_message(data["log_03"])

@tasks.loop(seconds=5)
async def loop():
    global check_game_server , old_player_ids , new_player_ids , active_channel

    active_channel = client.get_channel(int(active_channel_id))
    if active_channel is None: 
        print(data["Error_log_04"])
        return  
    if MCRcon_command.check():
        if  os.getenv('steam_api') == False:
            player_list = MCRcon_command.player_status()
            print(player_list)
            if not old_player_ids:
                old_player_ids = [player[0] for player in player_list] 
            else:
                old_player_ids = new_player_ids
                new_player_ids = [player[0] for player in player_list] 
            # 参加したプレイヤーを検出
            for player_id in new_player_ids:
                if player_id not in old_player_ids:
                    
                    server_name=steam_search.find_name_by_id(player_id,player_list)

                    login_message=f'{server_name}{data["join_the_game"]}'
                    MCRcon_command.calc(f'Broadcast {login_message}')
                    await active_channel.send(login_message)
                    print(login_message)
            # 退出したプレイヤーを検出
            for player_id in old_player_ids:
                if player_id not in new_player_ids:
                    print(player_id)
                    server_name=steam_search.find_name_by_id(player_id,player_list)

                    login_message=f'{server_name}{data["left_the_game"]}'
                    MCRcon_command.calc(f'Broadcast {login_message}')
                    await active_channel.send(login_message)
                    print(login_message)
        else:
            player_list = MCRcon_command.player_status()
            if not old_player_ids:
                old_player_ids = player_list
            else:
                old_player_ids = new_player_ids
                new_player_ids = player_list
                # 参加したプレイヤーを検出
            for player_id in new_player_ids:
                if player_id not in old_player_ids:
                    steam_name=steam_search.steam_id_name(player_id)
                    if steam_name:
                        login_message=f'{steam_name}{data["join_the_game"]}'
                        MCRcon_command.calc(f'Broadcast {login_message}')
                        await active_channel.send(login_message)
                        print(login_message)

            for player_id in old_player_ids:
                if player_id not in new_player_ids:
                    try:
                        steam_name=steam_search.steam_id_name(player_id)
                    except Exception as e:
                        print("steam Error")
                        return None
                    if steam_name:
                        login_message=f'{steam_name}{data["left_the_game"]}'
                        MCRcon_command.calc(f'Broadcast {login_message}')
                        await active_channel.send(login_message)
                        print(login_message)
    elif check_game_server:
        check_game_server=False
        await active_channel.send(data["stop_message"])

client.run(token)