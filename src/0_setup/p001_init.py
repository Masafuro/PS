import common.variables as var

def execute():
    # システムに名前を付け、初期化完了フラグを立てる
    var.system_name = "Python-PLC-v1"
    var.is_initialized = True
    print(f"Setup Complete: {var.system_name}")