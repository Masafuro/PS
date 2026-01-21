from variables import master_var as v

def execute():
    # システムの初期状態をマスター変数に直接書き込みます
    print("Setup: システム変数を初期化しています...")
    
    v.loop.cycle_count = 0
    v.loop.system_status = "Initializing"
    
    # 本来はここでハードウェアのチェックや通信の確立確認などを行います
    v.keep.server_connected = False
    v.keep.error_code = 0
    
    v.loop.system_status = "Running"
    print(f"Setup: 準備が完了しました。ステータス: {v.loop.system_status}")