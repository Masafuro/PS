from variables import master_var as v

def execute():
    # 終了処理を開始し、安全な停止状態へ移行します
    print("Teardown: 安全停止シーケンスを開始します...")
    
    # 稼働ステータスを停止に変更し、全てのフラグをリセットします
    v.loop.system_status = "Terminated"
    v.keep.server_connected = False
    
    # 実際にはここでファイルクローズやGPIOの解放などを行います
    print(f"Teardown: 最終サイクル数: {v.loop.cycle_count}")
    print("Teardown: 全てのプロセスが安全に終了しました。")