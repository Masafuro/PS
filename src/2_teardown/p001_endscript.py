from variables import master_var as v

def execute():
    print("\n--- Final Integrity Check ---")
    
    # 各領域の「真の値」を判定
    print(f"LOOP領域 (Expected: Counted) : {v.loop.counter}")
    print(f"KEEP領域 (Expected: ACTIVE)  : {v.keep.status}")
    
    # master.max_speed が 2000 であれば、Loop側の攻撃(0)を防げている
    print(f"MASTER領域(Expected: 2000)   : {v.master.max_speed}")
    print(f"MASTER領域(Expected: localhost): {v.master.server_url}")
    
    # system.version が 1.0.0 であれば、全員の攻撃を防げている
    print(f"SYSTEM領域(Expected: 1.0.0)  : {v.system.version}")
    print(f"SYSTEM領域(Expected: Custom...): {v.system.vendor}")
    
    print("------------------------------")