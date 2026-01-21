import yaml
import os
import config
from var_engine import VariableWorkspace, KeepWorkspace

master_var = None
loop_var = None
keep_var = None

def initialize():
    global master_var, loop_var, keep_var
    
    if not os.path.exists(config.VAR_YAML_PATH):
        raise FileNotFoundError(f"YAML not found: {config.VAR_YAML_PATH}")

    with open(config.VAR_YAML_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # 全ての権限を持つマスター
    master_var = VariableWorkspace(data)
    # Loop用の隔離された作業領域
    loop_var = VariableWorkspace(data)
    # Keep用の、読み取り保護されたアクセス窓口
    keep_var = KeepWorkspace(master_var)

initialize()