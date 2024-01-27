from mcrcon import MCRcon
from dotenv import load_dotenv
import os

# .envから環境変数を読み込む
load_dotenv()
#IP
server_address = os.getenv('server_address')
#password
server_pass = os.getenv('server_pass')
#port
server_port = int(os.getenv('server_port'))

server_error_log01 = os.getenv('server_error_log01')
server_error_log02 = os.getenv('server_error_log02')
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