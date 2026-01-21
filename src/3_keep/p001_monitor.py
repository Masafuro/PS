import time
from variables import master_var

def execute():
    # 3秒おきに server_connected を True と False で切り替える
    status = False
    while True:
        status = not status
        master_var.keep.server_connected = status
        print(f"  [Keep Process] Set master to: {status}")
        time.sleep(0.5)