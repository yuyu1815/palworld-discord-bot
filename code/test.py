import steam_search 
from mcrcon import MCRcon
from dotenv import load_dotenv
import subprocess
import os

import steam_search
import MCRcon_command
#IP
server_address = "119.228.195.76"
#password
server_pass = "adminkokoa"
#port
server_port = "32235"
#time out
MCRcon_time_out = "0.2"

system_os="Windows"
player_id='1952193462'
def main():
    id_to_find=MCRcon_command.player_status()
    single_player_id = player_id[0] if isinstance(player_id, list) else player_id
    id=steam_search.find_name_by_id(single_player_id,id_to_find)
    print(id)

main()