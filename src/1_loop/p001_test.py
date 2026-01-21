from variables import loop_var as v

def execute():
    # 実行前の値を表示します。隔離が成功していれば、keep.statusは常にリセットされているはずです。
    print(f"[Loop] Before: loop.counter={v.loop.counter}, keep.status={v.keep.status}")
    
    # 1. 自分の領域を正しく更新します（これはマスターに反映されるはずです）
    v.loop.counter += 1
    
    # 2. 相手の領域をわざと書き換えます（これは次のサイクルで破棄されるはずです）
    v.keep.status = "LOOP_HACKED"
    
    # 実行後の値を表示します
    print(f"[Loop] After : loop.counter={v.loop.counter}, keep.status={v.keep.status}")