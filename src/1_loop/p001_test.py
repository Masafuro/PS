from variables import loop_var as v

def execute():
    v.loop.cycle_count += 1
    # 書き換える「前」の状態を表示する
    # もしリセットが成功していれば、ここは毎回 False (またはYAMLの初期値) になるはず！
    print(f"--- Cycle {v.loop.cycle_count} Start ---")
    print(f"Before Hack: {v.keep.server_connected}")
    
    # ここで汚染してみる
    v.keep.server_connected = "HACKED!"
    print(f"After Hack : {v.keep.server_connected}")