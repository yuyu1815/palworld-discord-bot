from dotenv import load_dotenv
import os
import threading
import time
import subprocess
import json

import discord_bot
import MCRcon_command

load_dotenv()
discord_is_use=os.getenv('discord')
status_time=os.getenv('status_time')
folder_pach=os.getenv('folder_pach')
system_os=os.getenv('system_os')
port=os.getenv('port')
Language=os.getenv('Language')

server_status=False

with open(f"./Language/{Language}", 'r', encoding='utf-8') as file:
    data = json.load(file)

def sab_chec():
    for server_status in True:
        server_status = MCRcon_command.check()
        time.sleep(status_time)
    
def server_start():
    if system_os is "Linux":
        subprocess.run([f'{folder_pach}/PalServer.sh', f'port={port}','-useperfthreads','-NoAsyncLoadingThread','-UseMultithreadForDS'])
    elif system_os is "Windows":
        subprocess.run([f'{folder_pach}/PalServer.exe', f'port={port}','-useperfthreads','-NoAsyncLoadingThread','-UseMultithreadForDS'])
    else:
        print(data["Error_log_03"])
#リスタート
def server_restart():
    log=MCRcon_command.calc("Shutdown")
    server_start()

if __name__ == "__main__":
    #discord
    if discord_is_use is True:
        threading.Thread(target=discord_bot.discord_main)
        if server_status is True:
            threading.Thread(target=sab_chec)
            