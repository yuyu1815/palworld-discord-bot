from dotenv import load_dotenv
import os
import threading
import time
import subprocess
import json

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
            subprocess.run(f'{folder_pach}/PalServer.sh', f'port={port}','-useperfthreads','-NoAsyncLoadingThread','-UseMultithreadForDS', shell=True)
        elif system_os == "Windows":
            subprocess.run(f'{folder_pach}/PalServer.exe', f'port={port}','-useperfthreads','-NoAsyncLoadingThread','-UseMultithreadForDS', shell=True)
        else:
            print(data["Error_log_03"])
    else:
        print(data["Error_log_02"])
#リスタート
def server_restart():
    log=MCRcon_command.calc("Shutdown")
    server_start()

def discord_command():
    if system_os == "Linux":
        subprocess.run('python3 discord_bot.py', shell=True)
    elif system_os == "Windows":
        subprocess.run('py discord_bot.py', shell=True)
    else:
        print(data["Error_log_03"])

def gammelogin():
    print("テスト用")

def check_login_changes(new_logins):
    # ログイン情報をプレイヤーIDをキーとした辞書に変換する
    current_login_dict = {user['playeruid']: user['name'] for user in current_logins}
    new_login_dict = {user['playeruid']: user['name'] for user in new_logins}

    # 新しく追加されたユーザーを検出
    added_users = new_login_dict.keys() - current_login_dict.keys()
    # 退出したユーザーを検出
    removed_users = current_login_dict.keys() - new_login_dict.keys()
    
    # 新しく追加されたユーザーを表示
    for user_id in added_users:
        user_name = new_login_dict[user_id]
        user_return_data=f"{user_name}{data['join_the_ganme']}"
        print(user_return_data)


    # 退出したユーザーを表示
    for user_id in removed_users:
        user_name = current_login_dict[user_id]
        user_return_data=f"{user_name}{data['join_the_ganme']}"
        print(user_return_data)
    return user_return_data
if __name__ == "__main__":
    #discord
    server_status_update=threading.Thread(target=discord_command)
    server_status_update.start()
    print("sab")