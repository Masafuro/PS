from variables import master_var as v

def execute():
    print("=== Setup Phase: Initial Baseline ===")
    # YAMLから読み込まれた直後の値を表示
    print(f"[Initial] loop.counter    : {v.loop.counter}")
    print(f"[Initial] keep.status     : {v.keep.status}")
    print(f"[Initial] master.max_speed: {v.master.max_speed}")
    print(f"[Initial] system.version  : {v.system.version}")
    
    print("\n--- Setup Phase: Modification Attempt ---")
    # 1. master領域の書き換え（管理者権限として許可されるべき操作）
    v.master.max_speed = 2000
    print(f"Action: Set master.max_speed to 2000")

    # 2. system領域（憲法）の書き換え試行（拒否されるべき操作）
    v.system.version = "HACKED_BY_SETUP"
    print(f"Action: Try set system.version to 'HACKED_BY_SETUP'")
    
    print("\n--- Setup Phase: Results in Setup Session ---")
    # このセッション内での見え方を確認
    print(f"[Result] master.max_speed: {v.master.max_speed} (Should be 2000)")
    print(f"[Result] system.version  : {v.system.version} (Should still be 1.0.0)")
    print("========================================\n")