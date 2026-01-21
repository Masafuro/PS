import yaml
import os
import config
from var_engine import VariableWorkspace

# 外部からインポートされるグローバルインスタンス
master_var = None
loop_var = None
keep_var = None

def initialize():
    """システムの起動時に一度だけ呼び出される初期化関数"""
    global master_var, loop_var, keep_var
    
    if not os.path.exists(config.VAR_YAML_PATH):
        raise FileNotFoundError(f"YAML not found: {config.VAR_YAML_PATH}")

    with open(config.VAR_YAML_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # クラス定義に基づいてインスタンスを生成
    master_var = VariableWorkspace(data)
    loop_var = VariableWorkspace(data)
    keep_var = VariableWorkspace(data)

# インポート時に自動的に初期化を実行
initialize()