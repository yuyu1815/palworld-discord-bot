from steam import Steam
from dotenv import load_dotenv
import os
import json

# 環境変数 'steam_api_key' からAPIキーを取得
load_dotenv()
steam_api_key = os.getenv('steam_api_key')
Language = os.getenv('Language')

with open(f"./Language/{Language}", 'r', encoding='utf-8') as file:
    data = json.load(file)
# APIキーの存在をチェック
    
def steam_id_name(steam_id):
    if steam_api_key is None:
        print(data['server_error_log05'])

    steam = Steam(steam_api_key)
    user_details = steam.users.get_user_details(steam_id)
    personaname = user_details['player']['personaname']
    return personaname

def find_name_by_id(id_to_find, pairs_list):
    for id, name in pairs_list:
        if id == id_to_find:
            return name