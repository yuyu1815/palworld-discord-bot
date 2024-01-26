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
server_port = os.getenv('server_port')

def calc(cm):
    with MCRcon(server_address, server_pass, server_port) as mcr:
                log=mcr.command(cm)
                return log

def check():
    try:
        with MCRcon(server_address, server_pass, server_port) as mcr:
            log = mcr.command("Info")
            if log:  
                return True
            else:  
                return False
    except Exception as e:  
        print("server is offline")
        return False
    
def Player_check():
    with MCRcon(server_address, server_pass, server_port) as mcr:
                log=mcr.command("ShowPlayers")
                return log
