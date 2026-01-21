import time
from variables import keep_var as v

def execute():
    while True:
        time.sleep(0.5)
        
        # 1. 自分の領域を正しく更新します
        v.keep.status = "ACTIVE" if v.keep.status != "ACTIVE" else "IDLE"
        
        # 2. 相手の領域をわざと書き換えます（Loopのコミットによって上書きされるはずです）
        v.loop.counter = -999
        
        print(f"  [Keep] Update: keep.status={v.keep.status}, Try hack loop.counter=-999")