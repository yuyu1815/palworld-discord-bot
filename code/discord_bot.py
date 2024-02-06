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

check_game_server = False
old_players_list = [(None,None)]
active_channel_id = None
with open(f"./Language/{Language}", 'r', encoding='utf-8') as file:
    data = json.load(file)

with open(f"./channel_id.json", 'r', encoding='utf-8') as file:
    try:
        active_channel_json = json.load(file)
    except Exception as e:
        active_channel_json = {}
if active_channel_json:
    try:
        active_channel_id=active_channel_json['channel']
        active_channel = client.get_channel(int(active_channel_id))
    except Exception as e:
        active_channel_id=None

    

@client.event
async def on_ready():
    print("discord bot lady")
    await tree.sync()#スラッシュコマンドを同期
    loop.start()
    check_game_server=False

#test command
@tree.command(name="test",description="test")
async def test_command(interaction: discord.Interaction):
    # Embedインスタンスを作成し、色を青に設定
    await interaction.response.send_message(embed=discord.Embed(description=f"Channelid:{interaction.channel.id}\nchannel<#{active_channel_id}>\nrole<@&{active_channel_json['roleid']}>", color=discord.Color.blue()),ephemeral=True)
#ロール作成
@tree.command(name="createroll",description=data["createroll"])
async def rollcreate_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name="Pal Admin")
    if not role:
        guild = interaction.guild
        await guild.create_role(name="Pal Admin")
        role = discord.utils.get(interaction.guild.roles, name="Pal Admin")
        active_channel_json['roleid'] = role.id
        await interaction.response.send_message(embed=discord.Embed(description=f"{data['createroll_log01']}", color=discord.Color.green()),ephemeral=True)
    else:
        await interaction.response.send_message(embed=discord.Embed(description=f"{data['createroll_log02']}", color=discord.Color.red()),ephemeral=True)
    with open('./channel_id.json', 'w',encoding='utf-8') as f:
        json.dump(active_channel_json, f)
#help
@tree.command(name="help",description=data["help_info"])
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(data["help_list"],ephemeral=True)

#サーバーにコマンド送信
@tree.command(name="command",description=data["command"])
async def MCR_command(interaction: discord.Interaction,command: str):
    
    if discord.utils.get(interaction.guild.roles, id=int(active_channel_json['roleid'] or "0")) in interaction.user.roles or interaction.user.id == int(os.getenv('discord_id') or "0") or interaction.user.guild_permissions.administrator:
        if interaction.channel.id == active_channel_id and active_channel_id:
            if command.lower() != command.find('shutdown') and command.lower() != command.find('doexit'):
                command_log=MCRcon_command.calc(command)
                try:
                    if command_log:
                        await interaction.response.send_message(embed=discord.Embed(description=command_log, color=discord.Color.blue()),ephemeral=True)
                    else:
                        await interaction.response.send_message(embed=discord.Embed(description=data["Error_log_01"], color=discord.Color.red()),ephemeral=True)
                except Exception as e:
                    print(data["Error_log_01"])
                    await interaction.response.send_message(embed=discord.Embed(description=data["Error_log_01"], color=discord.Color.red()),ephemeral=True)
            else:
                await interaction.response.send_message(embed=discord.Embed(description=data["log_02"], color=discord.Color.red()),ephemeral=True)
        elif active_channel_id:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_05"], color=discord.Color.red()),ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_06"], color=discord.Color.red()),ephemeral=True)
    else:
        await interaction.response.send_message(embed=discord.Embed(description=data["log_07"], color=discord.Color.red()),ephemeral=True)
#開始コマンド
@tree.command(name="start",description=data["start"])
async def start_command(interaction: discord.Interaction):
    if discord.utils.get(interaction.guild.roles, id=int(active_channel_json['roleid'] or "0")) in interaction.user.roles or interaction.user.id == int(os.getenv('discord_id') or "0") or interaction.user.guild_permissions.administrator:
        if interaction.channel.id == active_channel_id and active_channel_id:
            if folder_pach:
                check_game_server=True
                await interaction.response.send_message(embed=discord.Embed(description=data["log_01"], color=discord.Color.green()),ephemeral=True)
                game_server_start=threading.Thread(target=main.server_start)
                game_server_start.start()
            else:
                await interaction.response.send_message(data["Error_log_02"],ephemeral=True)
        elif active_channel_id:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_05"], color=discord.Color.red()),ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_06"], color=discord.Color.red()),ephemeral=True)
    else:
        await interaction.response.send_message(embed=discord.Embed(description=data["log_07"], color=discord.Color.red()),ephemeral=True)

#停止コマンド
@tree.command(name="stop",description=data["stop"])
async def stop_command(interaction: discord.Interaction):
    if discord.utils.get(interaction.guild.roles, id=int(active_channel_json['roleid'] or "0")) in interaction.user.roles or interaction.user.id == int(os.getenv('discord_id') or "0") or interaction.user.guild_permissions.administrator:
        if interaction.channel.id == active_channel_id and active_channel_id:
            if MCRcon_command.check():
                shutdown_message=data['shutdown_message']
                stop=MCRcon_command.calc(f'Shutdown 30 {shutdown_message}')
                if stop :
                    await interaction.response.send_message(data["stop_message"],ephemeral=True)
                    await interaction.response.send_message(embed=discord.Embed(description=data["stop_message"], color=discord.Color.red()),ephemeral=True)

                else:
                    await interaction.response.send_message(embed=discord.Embed(description=data["server_error_log02"], color=discord.Color.red()),ephemeral=True)
            else:
                await interaction.response.send_message(embed=discord.Embed(description=data["server_error_log01"], color=discord.Color.red()),ephemeral=True)
        elif active_channel_id:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_05"], color=discord.Color.red()),ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_06"], color=discord.Color.red()),ephemeral=True)
    else:
        await interaction.response.send_message(embed=discord.Embed(description=data["log_07"], color=discord.Color.red()),ephemeral=True)

#Restart
@tree.command(name="restart",description=data["restart"])
async def update_command(interaction: discord.Interaction):
    if discord.utils.get(interaction.guild.roles, id=int(active_channel_json['roleid'] or "0")) in interaction.user.roles or interaction.user.id == int(os.getenv('discord_id') or "0") or interaction.user.guild_permissions.administrator:
        if interaction.channel.id == active_channel_id and active_channel_id:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_04"], color=discord.Color.green()),ephemeral=True)
            main.server_restart()
        elif active_channel_id:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_05"], color=discord.Color.red()),ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_06"], color=discord.Color.red()),ephemeral=True)  
    else:
        await interaction.response.send_message(embed=discord.Embed(description=data["log_07"], color=discord.Color.red()),ephemeral=True)


#update
@tree.command(name="update",description=data["update"])
async def update_command(interaction: discord.Interaction):
    if discord.utils.get(interaction.guild.roles, id=int(active_channel_json['roleid'] or "0")) in interaction.user.roles or interaction.user.id == int(os.getenv('discord_id') or "0") or interaction.user.guild_permissions.administrator:
        if interaction.channel.id == active_channel_id and active_channel_id:
            if MCRcon_command.check():
                try:
                    subprocess.run('steamcmd +login anonymous +app_update 2394010 validate +quit')
                    await interaction.response.send_message(embed=discord.Embed(description=data["update_log02"], color=discord.Color.green()),ephemeral=True)
                except Exception as e:
                    await interaction.response.send_message(embed=discord.Embed(description=data["server_error_log04"], color=discord.Color.red()),ephemeral=True)
            else:
                await interaction.response.send_message(embed=discord.Embed(description=data["server_error_log03"], color=discord.Color.red()),ephemeral=True)
        elif active_channel_id:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_05"], color=discord.Color.red()),ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(description=data["log_06"], color=discord.Color.red()),ephemeral=True)
    else:
        await interaction.response.send_message(embed=discord.Embed(description=data["log_07"], color=discord.Color.red()),ephemeral=True)

#channel設定
@tree.command(name="channel",description=data["active_channel"])
async def update_command(interaction: discord.Interaction):
    if discord.utils.get(interaction.guild.roles, id=int(active_channel_json['roleid'] or "0")) in interaction.user.roles or interaction.user.id == int(os.getenv('discord_id') or "0") or interaction.user.guild_permissions.administrator:
        global active_channel_id
        active_channel_json["channel"]=interaction.channel.id
        with open('./channel_id.json', 'w',encoding='utf-8') as f:
            json.dump(active_channel_json, f)

        active_channel_id=active_channel_json['channel']
        await interaction.response.send_message(embed=discord.Embed(description=data["log_03"], color=discord.Color.green()),ephemeral=True)
    else:
        await interaction.response.send_message(embed=discord.Embed(description=data["log_07"], color=discord.Color.red()),ephemeral=True)

@tasks.loop(seconds=3)
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
                        embed = discord.Embed(description=f"{login_message}", color=discord.Color.blue())
                        await active_channel.send(embed=embed)
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
                        embed = discord.Embed(description=f"{logout_message}", color=discord.Color.orange())
                        await active_channel.send(embed=embed)
            old_players_list = new_players_list

        elif check_game_server:
            check_game_server=False
            await active_channel.send(embed=discord.Embed(description=f"{data['stop_message']}"), color=discord.Color.red())

client.run(token)