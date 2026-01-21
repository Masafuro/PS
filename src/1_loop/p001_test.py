from variables import loop_var as v

def execute():
    # 1. 自分の領域を更新
    v.loop.counter += 1
    
    # 2. 相手（master/system）への攻撃を試みる
    # これらは loop_var 内では変わるが、コミットされないためマスターは無傷なはず
    v.master.max_speed = 0
    v.system.version = "HACKED_BY_LOOP"
    
    if v.loop.counter % 10 == 0:
        print(f"[Loop] Cycle: {v.loop.counter} | speed_ref: {v.master.max_speed}")