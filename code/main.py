from dotenv import load_dotenv
import os
import threading
import time

import discord_bot
import check
import MCRcon_command

load_dotenv()
discord_is_use=os.getenv('discord')
status_time=os.getenv('status_time')
server_status=False

def sab_chec():
    for server_status in True:
        server_status = check.calc()
        time.sleep(status_time)
    

if __name__ == "__main__":
    #discord
    if discord_is_use is True:
        threading.Thread(target=discord_bot.discord_main)
        if server_status is True:
            threading.Thread(target=sab_chec)
    
    

    