import time
from variables import keep_var as v

def execute():
    """
    Keepフェーズの動作確認スクリプト。
    自身の領域の更新と、他領域への書き換え試行、およびその結果を出力します。
    """
    while True:
        # 画面がログで埋め尽くされないよう、1秒間隔で実行します
        time.sleep(1.0)
        
        # 1. 自身の領域（keep）を正しく更新
        v.keep.status = "ACTIVE"
        
        # 2. 読み取り専用領域（master / system）への上書きを試行
        # これらは内部的にコピーに対して操作が行われるため、マスターには届きません
        v.master.server_url = "http://malicious.site"
        v.system.vendor = "HACKER_CORP"
        
        # 実行したアクションと、その直後の変数の見え方を出力
        print(f"  [Keep] --- Attempting Domain Updates ---")
        print(f"  [Keep] Self Update  -> status: {v.keep.status} (Expected: ACTIVE)")
        print(f"  [Keep] Master Attack -> url: {v.master.server_url} (Expected: localhost...)")
        print(f"  [Keep] System Attack -> vendor: {v.system.vendor} (Expected: Custom Factory...)")
        print(f"  [Keep] ---------------------------------")