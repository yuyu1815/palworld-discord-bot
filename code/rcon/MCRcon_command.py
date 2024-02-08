from mcrcon import MCRcon
from dotenv import load_dotenv
import subprocess
import os

# .envから環境変数を読み込む
load_dotenv()
#IP
server_address = "192.168.3.5"
#password
server_pass = "adminkokoa"
#port
server_port = "32235"
#time out
MCRcon_time_out = 1

steam_api = True
server_error_log01 = "aaa"
server_error_log02 = "bbb"




#タイムアウトチェック
def check():
    script_dir = os.getcwd()
    rcon_path=f'{script_dir}/rcon.exe'
    print(script_dir)
    players_data = subprocess.run(
        f'{rcon_path} -a {server_address}:{server_port} -p {server_pass} -T {MCRcon_time_out}s ShowPlayers',
        shell=True,
        capture_output=True
    )
    output = players_data.stdout.decode()
    return output

def player_status():

    script_dir = os.getcwd()
    rcon_path=f'{script_dir}/rcon.exe'
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
    
print(player_status())