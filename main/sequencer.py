import importlib.util
import os
import sys
import time
import threading

# ==========================================
# システム設定（ここを調整して動作を変える）
# ==========================================

# 1. フォルダ名の定義
SRC_DIR_NAME = "src"
DIR_SETUP    = "0_setup"
DIR_LOOP     = "1_loop"
DIR_TEARDOWN = "2_teardown"
DIR_KEEP     = "3_keep"

# 2. 実行設定
# スキャンサイクルの合間に挟む休憩時間（秒）
CYCLE_WAIT_TIME = 0.01

# 3. 読み込むファイルの拡張子
SCRIPT_EXTENSION = ".py"

# ==========================================
# 内部処理
# ==========================================

# プロジェクトのルートディレクトリ設定
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_execute_functions(phase_folder):
    """指定されたフェーズのフォルダからexecute関数を抽出する"""
    funcs = []
    # フォルダパスの組み立て： (PROJECT_ROOT)/(SRC_DIR_NAME)/(phase_folder)
    target_dir = os.path.join(PROJECT_ROOT, SRC_DIR_NAME, phase_folder)
    
    if not os.path.exists(target_dir):
        return funcs

    # ファイル名でソートして順序を保証。拡張子も変数を使用。
    files = sorted([f for f in os.listdir(target_dir) if f.endswith(SCRIPT_EXTENSION)])
    
    for file_name in files:
        file_path = os.path.join(target_dir, file_name)
        # モジュール名が重複しないよう、フェーズ名をプレフィックスにする
        module_name = f"{phase_folder}_{file_name[:-len(SCRIPT_EXTENSION)]}"
        
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'execute'):
            funcs.append((file_name, module.execute))
    
    return funcs

def main():
    print("Python Sequencer Starting...")

    # 1. Phase 0: Setup（初期化）
    print(f"\n[{DIR_SETUP}] Initializing setup scripts...")
    setup_tasks = get_execute_functions(DIR_SETUP)
    for name, func in setup_tasks:
        print(f"Running setup: {name}")
        func()

    # 2. Phase 3: Keep（常駐タスク起動）
    print(f"\n[{DIR_KEEP}] Starting keep-alive tasks...")
    keep_tasks = get_execute_functions(DIR_KEEP)
    for name, func in keep_tasks:
        print(f"Starting background thread: {name}")
        t = threading.Thread(target=func, name=name, daemon=True)
        t.start()

    # 3. Phase 1: Loop（メインサイクル）
    print(f"\n[{DIR_LOOP}] Entering main loop cycle...")
    loop_tasks = get_execute_functions(DIR_LOOP)
    
    if not loop_tasks:
        print(f"Warning: No scripts found in {DIR_LOOP}.")

    try:
        while True:
            for name, func in loop_tasks:
                func()
            # 設定した待機時間を使用
            time.sleep(CYCLE_WAIT_TIME)
            
    except KeyboardInterrupt:
        print("\nStop signal received. Shutting down...")

    # 4. Phase 2: Teardown（終了処理）
    print(f"\n[{DIR_TEARDOWN}] Running teardown scripts...")
    teardown_tasks = get_execute_functions(DIR_TEARDOWN)
    for name, func in teardown_tasks:
        print(f"Running teardown: {name}")
        func()

    print("\nPython Sequencer has safely stopped.")

if __name__ == "__main__":
    main()