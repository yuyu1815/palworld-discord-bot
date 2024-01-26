import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import json

load_dotenv()
intents = discord.Intents.all()
intents.guilds = True
intents.guild_messages = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
token=os.getenv('token')
Language=os.getenv('Language')

with open(f"./Language/{Language}", 'r', encoding='utf-8') as file:
    data = json.load(file)

@client.event
async def on_ready():
    print("lady")
    await tree.sync()#スラッシュコマンドを同期
@tree.command(name="help",description=data["help_info"])
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message(data["help_list"],ephemeral=True)

def discord_main():
    client.run(token)