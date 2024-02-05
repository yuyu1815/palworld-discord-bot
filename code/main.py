from dotenv import load_dotenv
import os
import time
import subprocess
import json
import threading
import time

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
#生きているかチェック
def sab_chec():
        server_status = MCRcon_command.check()
        time.sleep(status_time)
#startcommand   
def server_start():
    if folder_pach:
        if system_os == "Linux":
            print("Linux")
            subprocess.run(f'{folder_pach}/PalServer.sh port={port} -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS', shell=True)
        elif system_os == "Windows":
            print("Windows")
            subprocess.run(f'{folder_pach}/PalServer.exe port={port} -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS', shell=True)
        else:
            print(data["Error_log_03"])
    else:
        print(data["Error_log_02"])
#リスタート
def server_restart():
    MCRcon_command.calc("Shutdown")
    time.sleep(3)
    server_start()

def discord_command():
    if system_os == "Linux":
        subprocess.run('python3 discord_bot.py', shell=True)
    elif system_os == "Windows":
        subprocess.run('py discord_bot.py', shell=True)
    else:
        print(data["Error_log_03"])

def is_list(var):
    return isinstance(var, list)

# 変数が複数のリスト（配列）を含むかどうかをチェックする関数
def contains_multiple_lists(var):
    if is_list(var) and all(is_list(elem) for elem in var):
        return True
    return False
    
if __name__ == "__main__":
    #discord
    server_discord=threading.Thread(target=discord_command)
    server_discord.start()
    print("Ok")