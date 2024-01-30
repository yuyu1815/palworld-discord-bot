from steam import *
from dotenv import load_dotenv
import os
import json
import re

# 環境変数 'steam_api_key' からAPIキーを取得
load_dotenv()
Language = os.getenv('Language')

with open(f"./Language/{Language}", 'r', encoding='utf-8') as file:
    data = json.load(file)
# APIキーの存在をチェック
    
def steam_id_name(steam_id):
    return None
    try:
        steam_id_num = steam_id
    except ValueError:
        #print(f"エラー: steam_id '{steam_id}' は数値に変換できません。")
        return None

    user_details = steam.users.get_user_details(steam_id_num)

    # user_response["players"] が空ではないことを確認します。
    if not user_details["players"]:
        #print(f"プレイヤーID {steam_id} に対する詳細情報が見つかりませんでした。")
        return None

    # プレイヤー情報が存在する場合、最初のプレイヤーの情報を返します。
    return {"player": user_details["players"][0]}


def find_name_by_id(id_to_find, pairs_list):
    print(f"id_to_find:{id_to_find} pairs_list{pairs_list}")
    for name,id in pairs_list:
        if id == id_to_find:
            return name
        
