# 仮のdata辞書を作成します。実際の環境で適切な値が設定されていることを確認してください。
data = {"join_the_game": "さんがゲームに参加しました！"}

# プレイヤーのステータスを取得します（仮の関数を使用します）。
new_players_list = [('win11から国民を守る会', '0000000000')]

# new_players_listが空でないことを確認します。
if new_players_list:
    for join_player_name, join_player_id in new_players_list:
        # IDが '00000000' に一致するかをチェックします。
        # IDが正しい桁数になっていることを確認してください。
        if join_player_id == '0000000000':
            login_message = f'{join_player_name}{data["join_the_game"]}'
            print(login_message)