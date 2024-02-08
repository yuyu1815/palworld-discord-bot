import discord
from discord import app_commands
from discord.ext import tasks
from discord.utils import get

from dotenv import load_dotenv
import os
import json
import threading
import subprocess
import asyncio
import sys

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
system_os=os.getenv('system_os')

check_game_server = False
old_players_list = [(None,None)]
active_channel_id = None

if system_os == "Linux":
    win_linu_folder_pach="."
elif system_os == "Windows":
    win_linu_folder_pach=os.getcwd()
with open(f"{win_linu_folder_pach}/Language/{Language}", 'r', encoding='utf-8') as file:
    data = json.load(file)

with open(f"{win_linu_folder_pach}/channel_id.json", 'r', encoding='utf-8') as file:
    try:
        active_channel_json = json.load(file)
        active_channel_id = active_channel_json['channel']
        active_channel = client.get_channel(int(active_channel_id))
        
    except Exception as e:
        active_channel_json = {}
        active_channel_id = None
        active_channel = None

async def command_discord_say(interaction,description,color,ephemeral):
    await interaction.response.send_message(embed=discord.Embed(description=description, color=color),ephemeral=ephemeral)
    return
async def admin_roll(interaction):
    if not (discord.utils.get(interaction.guild.roles, id=int(active_channel_json['roleid'] or "0")) in interaction.user.roles or interaction.user.id == int(os.getenv('discord_id') or "0") or interaction.user.guild_permissions.administrator):
        await command_discord_say(interaction,data["log_07"],discord.Color.green(),True)
        return False
    elif not active_channel_id:
        await command_discord_say(interaction,data["log_06"],discord.Color.green(),True)
        return False
    elif not interaction.channel.id == active_channel_id:
        await command_discord_say(interaction,data["log_05"],discord.Color.green(),True)
        return False
    else:
        return True
        
@client.event
async def on_ready():
    print("discord bot lady")
    await tree.sync()#スラッシュコマンドを同期
    #loop.start()
    check_game_server=False

@tree.command(name="test",description="test")
async def test_command(interaction: discord.Interaction):
    # Embedインスタンスを作成し、色を青に設定
    discord_send_message=f"Channelid:{interaction.channel.id}\nchannel<#{active_channel_id}>\nrole<@&{active_channel_json['roleid']}>"
    await command_discord_say(interaction,discord_send_message,discord.Color.blue(),True)

#ロール作成
@tree.command(name="createroll",description=data["createroll"])
async def rollcreate_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name="Pal Admin")
    if not role:
        #ロール作成
        await interaction.guild.create_role(name="Pal Admin")
        #ロールチェック
        role = discord.utils.get(interaction.guild.roles, name="Pal Admin")
        #ロールid保存
        active_channel_json['roleid'] = role.id
        await command_discord_say(interaction,data['createroll_log01'],discord.Color.green(),True)
    else:
        await command_discord_say(interaction,data['createroll_log02'],discord.Color.red(),True)
    
    #上書き保存
    with open('./channel_id.json', 'w',encoding='utf-8') as f:
        json.dump(active_channel_json, f)

#help
@tree.command(name="help",description=data["help_info"])
async def help_command(interaction: discord.Interaction):
    await command_discord_say(interaction,data["help_list"],discord.Color.green(),True)

#コマンド送信
@tree.command(name="command",description=data["command"])
async def MCR_command(interaction: discord.Interaction,command: str):
    if await admin_roll(interaction):
        command_log=MCRcon_command.calc(command)
        if command_log:
            await command_discord_say(interaction,command_log,discord.Color.blue(),True)
        else:
            await command_discord_say(interaction,data["Error_log_01"],discord.Color.red(),True)
#開始コマンド
@tree.command(name="start",description=data["start"])
async def start_command(interaction: discord.Interaction):
    if await admin_roll(interaction):
        if folder_pach:
            check_game_server=True
            await command_discord_say(interaction,data["log_01"],discord.Color.green(),True)
            game_server_start=threading.Thread(target=main.server_start)
            game_server_start.start()
        else:
            await command_discord_say(interaction,data['Error_log_02'],discord.Color.red(),True)
#停止コマンド
@tree.command(name="stop",description=data["stop"])
async def stop_command(interaction: discord.Interaction):
    if await admin_roll(interaction):
        if MCRcon_command.check():
            shutdown_message=data['shutdown_message']
            stop=MCRcon_command.calc(f'Shutdown 30 {shutdown_message}')
            if stop :
                await command_discord_say(interaction,data['stop_message'],discord.Color.blue(),True)
            else:
                await command_discord_say(interaction,data['server_error_log02'],discord.Color.red(),True)
        else:
            await command_discord_say(interaction,data['server_error_log01'],discord.Color.red(),True)
#Restart
@tree.command(name="restart",description=data["restart"])
async def update_command(interaction: discord.Interaction):
    if await admin_roll(interaction):
        await command_discord_say(interaction,data['log_04'],discord.Color.green(),True)
        main.server_restart()
#update
@tree.command(name="update",description=data["update"])
async def update_command(interaction: discord.Interaction):
    if await admin_roll(interaction):
        if not MCRcon_command.check():
            try:
                await command_discord_say(interaction,data['update_log01'],discord.Color.green(),False)
                if system_os == "Linux":
                    subprocess.run(f'/home/steam/.steam/steamcmd/steamcmd.sh +force_install_dir "{folder_pach}" +login anonymous +app_update 2394010 validate +quit')
                elif system_os == "Windows":
                    subprocess.run(f'{os.getcwd()}/steamcmd/steamcmd.exe +force_install_dir "{folder_pach}" +login anonymous +app_update 2394010 validate +quit')
                active_channel = client.get_channel(int(active_channel_id))
                await active_channel.send(embed=discord.Embed(description=data['update_log02'], color=discord.Color.green()))
            except Exception as e:
                await command_discord_say(interaction,data['server_error_log04'],discord.Color.red(),True)
        else:
            await command_discord_say(interaction,data['server_error_log03'],discord.Color.red(),True)

#channel設定
@tree.command(name="channel",description=data["active_channel"])
async def update_command(interaction: discord.Interaction):
    if not (discord.utils.get(interaction.guild.roles, id=int(active_channel_json['roleid'] or "0")) in interaction.user.roles or interaction.user.id == int(os.getenv('discord_id') or "0") or interaction.user.guild_permissions.administrator):
        await command_discord_say(interaction,data["log_07"],discord.Color.green(),True)
    else:
        global active_channel_id
        active_channel_json["channel"]=interaction.channel.id
        with open('./channel_id.json', 'w',encoding='utf-8') as f:
            json.dump(active_channel_json, f)
        active_channel_id=active_channel_json['channel']
        await command_discord_say(interaction,data["log_03"],discord.Color.green(),True)

@tasks.loop(seconds=5)
async def loop():
    global active_channel, old_players_list
    try:
        active_channel = client.get_channel(int(active_channel_id))
    except Exception as e:
        #print(data["Error_log_04"])
        return
    if MCRcon_command.check():
        if os.getenv('send_message'):
            
            new_players_list = MCRcon_command.player_status()
            #login
            if old_players_list == [(None,None)]:
                old_players_list = new_players_list

            players_who_joined = [(name, playeruid) for name, playeruid in new_players_list if (name, playeruid) not in old_players_list]
            players_who_left = [(name, playeruid) for name, playeruid in old_players_list if (name, playeruid) not in new_players_list]

            for name,playeruid in players_who_joined: 
                if name :
                    if playeruid == '00000000':
                        if os.getenv('steam_api'):
                            login_message = f'{name}{data["join_the_game"]}'
                            server_login_message = f'{name}{data["server_join_the_game"]}'
                        else:
                            steam_name=steam_search.steam_id_name(name)
                            login_message = f'{steam_name}{data["join_the_game"]}'
                            server_login_message = f'{steam_name}{data["server_join_the_game"]}'
                        print(login_message)
                        MCRcon_command.calc(f'Broadcast {server_login_message}')
                        await active_channel.send(embed=discord.Embed(description=f"{login_message}", color=discord.Color.blue()))
                # 退出したプレイヤーに関して処理を行う
            for name, playeruid in players_who_left:
                if name :
                    if playeruid != '00000000':
                        if os.getenv('steam_api'):
                            logout_message = f'{name}{data["left_the_game"]}'
                            server_logout_message = f'{name}{data["server_left_the_game"]}'
                        else:
                            steam_name=steam_search.steam_id_name(name)
                            logout_message = f'{steam_name}{data["left_the_game"]}'
                            server_logout_message = f'{steam_name}{data["server_left_the_game"]}'

                        print(logout_message)
                        MCRcon_command.calc(f'Broadcast {server_logout_message}')
                        await active_channel.send(embed=discord.Embed(description=f"{logout_message}", color=discord.Color.orange()))
            old_players_list = new_players_list

        elif check_game_server:
            check_game_server=False
            await active_channel.send(embed=discord.Embed(description=f"{data['stop_message']}"), color=discord.Color.red())

client.run(token)