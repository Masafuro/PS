import time

# 前回の時刻を保存するための変数（初期値は None）
# この変数は関数の外にあるため、次のサイクルでも値を覚えています
last_time = None

def execute():
    global last_time
    
    # 高精度な現在時刻を取得
    current_time = time.perf_counter()
    
    if last_time is not None:
        # 今回の時刻 - 前回の時刻 = スキャンサイクルタイム
        duration = current_time - last_time
        
        # 画面の端に邪魔にならないように表示（. を打つスクリプトと共存）
        # ミリ秒単位に変換して表示します
        print(f"[Cycle Time: {duration * 1000:.2f} ms]")
    
    # 今回の時刻を「次回用」に保存
    last_time = current_time