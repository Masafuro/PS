import os
import sys

# 1. フォルダ名の定義
SRC_DIR_NAME = "src"
DIR_SETUP    = "0_setup"
DIR_LOOP     = "1_loop"
DIR_TEARDOWN = "2_teardown"
DIR_KEEP     = "3_keep"

# 2. 実行パラメータ
CYCLE_WAIT_MS = 100 
SCRIPT_EXTENSION = ".py"

# 3. パス設定
# config.pyがあるフォルダの1つ上がプロジェクトルート (PS/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# YAMLファイルの場所を定義
VAR_YAML_PATH = os.path.join(PROJECT_ROOT, SRC_DIR_NAME, "common", "variables.yaml")

# srcフォルダをsys.pathに追加
SRC_PATH = os.path.join(PROJECT_ROOT, SRC_DIR_NAME)
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)