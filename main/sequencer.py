import time
import threading
import os
import sys

# 自分のいるフォルダ(main)をパスに追加
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

import config
import loader
# 変数管理システムをインポート
import variables

def main():
    print(f"Sequencer Start (Wait: {config.CYCLE_WAIT_MS}ms)")

    # --- Phase 0: Setup ---
    # Setupはシステムの起動時なので、直接master_varを操作してもOKなフェーズ
    setup_tasks = loader.get_execute_functions(config.DIR_SETUP)
    for name, func in setup_tasks:
        func()

    # --- Phase 3: Keep ---
    # 非同期で動くKeepタスクを起動
    keep_tasks = loader.get_execute_functions(config.DIR_KEEP)
    for name, func in keep_tasks:
        threading.Thread(target=func, name=name, daemon=True).start()

    # --- Phase 1: Loop ---
    loop_tasks = loader.get_execute_functions(config.DIR_LOOP)
    try:
        while True:
            # 1. 【Snapshot】マスター掲示板から、Loop専用の作業机(loop_var)に全コピー
            variables.loop_var.sync_from(variables.master_var)

            # 2. 【Execute】ユーザースクリプトを実行
            # 各スクリプト内では from variables import loop_var して、この「机」を操作する
            for name, func in loop_tasks:
                func()

            # 3. 【Commit】Loopが担当する領域（loop領域）だけをマスターに反映
            # これにより、loop_var.keep領域への変更は捨てられ、masterは汚れない
            variables.loop_var.commit_to_master(variables.master_var)

            # 指定時間待機
            time.sleep(config.CYCLE_WAIT_MS / 1000.0)

    except KeyboardInterrupt:
        print("\nStopping...")

    # --- Phase 2: Teardown ---
    teardown_tasks = loader.get_execute_functions(config.DIR_TEARDOWN)
    for name, func in teardown_tasks:
        func()

if __name__ == "__main__":
    main()