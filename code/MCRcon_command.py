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
    try:
        with MCRcon(server_address, server_pass, server_port) as mcr:
            log=mcr.command(cm)
            return log
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
    elif system_os == "Windous":
        players_data = subprocess.run(
            f'./rcon/rcon.exe -a {server_address}:{server_port} -p {server_pass} -T {MCRcon_time_out}s ShowPlayers',
            shell=True,
            capture_output=True
        )

    # コマンドの出力をデコードして文字列として取得
    output = players_data.stdout.decode()

    # 出力を行ごとに分割
    players_lines = output.split('\n')

    # 各プレイヤー情報を格納するためのリストを初期化
    players_list = []
    steamid_list = []
    # 各プレイヤー情報を処理
    for player in players_lines:
        # 空行をスキップ
        if player.strip() == "":
            continue
        if 'name' in player.lower() and 'playeruid' in player.lower():
            continue
        # プレイヤーの情報をカンマで分割
        try:
            name, playeruid, steamid = player.split(',')
            # nameとplayeruidをタプルにしてリストに追加
            print("name,{name} playeruid,{playeruid}")
            players_list.append((name, playeruid))
            steamid_list.append(steamid)
        except ValueError as e:
            print(f"行の処理中にエラーが発生しました: {player}. エラー: {e}")
    print(f"steam:{steamid_list} players_list:{players_list}" )
    # 整形したリストを出力
    if steam_api:      
        return players_list
    else:
        return steamid_list