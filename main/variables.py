import yaml
import os
import config
from var_engine import VariableWorkspace, KeepWorkspace

# 外部からインポートされるグローバルインスタンス
# master_var: 全領域の実体を保持。system以外の書き換えが可能（setup/teardown用）
# loop_var:   1_loop専用の作業領域。サイクル終了時にloop領域のみコミットされる
# keep_var:   3_keep専用の窓口。keep領域は即時反映、他は読み取り専用
master_var = None
loop_var = None
keep_var = None

def initialize():
    """
    システムの起動時に一度だけ呼び出される初期化関数。
    YAMLから全ドメイン（loop, keep, master, system）の初期値を読み込み、
    それぞれの役割に応じたワークスペースを生成します。
    """
    global master_var, loop_var, keep_var
    
    if not os.path.exists(config.VAR_YAML_PATH):
        raise FileNotFoundError(f"YAML not found: {config.VAR_YAML_PATH}")

    with open(config.VAR_YAML_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # 全ての権限を持つマスター（実体）を生成
    # ※ var_engine側の制約により、これを通じても system 領域は破壊できません
    master_var = VariableWorkspace(data)
    
    # Loop用の隔離された作業領域を生成
    # 起動直後はマスターと同じ値を持ちますが、メモリ上は別体として切り離されます
    loop_var = VariableWorkspace(data)
    
    # Keep用のアクセス窓口を生成
    # master_varへの参照を渡し、内部でアクセス制限（ReadOnly等）をかけます
    keep_var = KeepWorkspace(master_var)

# インポート時に自動的に初期化を実行
initialize()