from variables import master_var as v

def execute():
    print("Teardown: 安全停止シーケンスを開始します...")
    
    # YAMLの定義に合わせて v.loop.counter を参照する
    print(f"Teardown: 最終サイクル数: {v.loop.counter}")
    
    print("Teardown: 全てのプロセスが安全に終了しました。")