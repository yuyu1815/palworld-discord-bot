from mcrcon import MCRcon
from dotenv import load_dotenv
import subprocess
import os

# .envから環境変数を読み込む
load_dotenv()
#IP
server_address = os.getenv('server_address')
#password
server_pass = os.getenv('server_pass')
#port
server_port = int(os.getenv('server_port'))
#time out
MCRcon_time_out = os.getenv('MCRcon_time_out')

steam_api = os.getenv('steam_api')
server_error_log01 = os.getenv('server_error_log01')
server_error_log02 = os.getenv('server_error_log02')
system_os=os.getenv('system_os')


#コマンド用
def calc(cm):
    if system_os == "Linux":
        with MCRcon(server_address, server_pass, server_port) as mcr:
            try:
                log=mcr.command(cm)
                return log
            except Exception as e:
                print(server_error_log01)
                return False
    elif system_os == "Windows":
        script_dir = os.getcwd()
        rcon_path=f'{script_dir}/rcon/rcon.exe'
        try:
            players_data = subprocess.run(
                f'{rcon_path} -a {server_address}:{server_port} -p {server_pass} "{cm}"',
                shell=True,
                capture_output=True
            )
            output = players_data.stdout.decode()
            return output
        except Exception as e:
            print(server_error_log01)
            return False
#タイムアウトチェック
def check():
    try:
        with MCRcon(server_address, server_pass, server_port) as mcr:
            log = mcr.command("a")
        if not log.find('Unknown command'):
            return True
        else:  
            print(server_error_log01)
            return False
    except Exception as e:
        return False
    
def player_status():
    if system_os == "Linux":
        players_data = subprocess.run(
            f'./rcon/rcon -a {server_address}:{server_port} -p {server_pass} -T {MCRcon_time_out}s ShowPlayers',
            shell=True,
            capture_output=True
        )
        output = players_data.stdout.decode()
    elif system_os == "Windows":
        script_dir = os.getcwd()
        rcon_path=f'{script_dir}/rcon/rcon.exe'
        print(script_dir)
        players_data = subprocess.run(
            f'{rcon_path} -a {server_address}:{server_port} -p {server_pass} -T {MCRcon_time_out}s ShowPlayers',
            shell=True,
            capture_output=True
        )
        output = players_data.stdout.decode()

    
    # 出力を行ごとに分割
    players_lines = output.split('\n')
    # 各プレイヤー情報を格納するためのリストを初期化
    players_list = []
    playeruid_list = []
    steamid_list = []
    # 各プレイヤー情報を処理
    for player in players_lines:
        # 空行をスキップ
        if player.strip() == "":
            continue
        #if 'name' in player.lower() and 'playeruid' in player.lower():
        #    continue
        # プレイヤーの情報をカンマで分割
        try:
            name, playeruid, steamid = player.split(',')
            # nameとplayeruidをタプルにしてリストに追加
            #print(f"name,{name} playeruid,{playeruid}")
            players_list.append((name, playeruid))
            #playeruid_list.append(playeruid)
            steamid_list.append((steamid,playeruid))
        except ValueError as e:
            print(f"player: {player}. Error: {e}")
    
    # 整形したリストを出力
    if steam_api:
        if players_list:
            #print(f"players_list :{players_list}")  
            return players_list
        else:
            #print(f"players_list :{players_list}")  
            return [("noname","1")]
    else:
        #print(f"steamid_list :{steamid_list}")  
        return steamid_list