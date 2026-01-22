# 共有変数アクセス 実装サンプル集

本フレームワークを利用するための `variables.yaml` の定義方法と、各実行フェーズにおけるスクリプトの記述例をまとめます。

## 0. variables.yaml の構成例

共有変数は `src/common/variables.yaml` で定義します。トップレベルのキーがそのままドメイン名（`loop`, `keep`, `master`, `system`）に対応します。

```yaml
# 1_loop が更新権限を持つ領域
loop:
  counter: 0
  auto_mode: false

# 3_keep が更新権限を持つ領域
keep:
  status: "Standby"
  last_heartbeat: 0

# 0_setup が初期化し、全員が参照する設定領域
master:
  max_speed: 1500
  server_url: "http://localhost:8080"
  timeout_ms: 5000

# システムが保護する不変の定数領域（憲法）
system:
  version: "1.0.0"
  model_id: "SEQ-001"
  vendor: "Custom Factory Solution"

```

---

## 1. 同期制御フェーズ（`1_loop`）

**使用する変数:** `loop_var`
**特徴:** 制御ロジックの整合性を保つための「スナップショット・コミット」方式。

```python
from variables import loop_var as v

def execute():
    # --- loopドメイン: 書き込み可能 ---
    # YAMLで定義した階層そのままにアクセスします。
    # 変更はサイクル終了時にマスターデータへ反映されます。
    v.loop.counter += 1

    # --- keep/master/systemドメイン: 読み取り専用（スナップショット） ---
    # 参照される値はサイクル開始時に固定されたものです。
    if v.keep.status == "ACTIVE":
        # 書き換えてもエラーにはなりませんが、マスターデータには反映されません。
        v.master.max_speed = 0  # 物理的に保護されます
        
    print(f"System Version: {v.system.version}")

```

---

## 2. 非同期通信・I/Oフェーズ（`3_keep`）

**使用する変数:** `keep_var`
**特徴:** 外部情報の即時反映と、他領域への「誤書き込み」に対する物理的な保護。

```python
import time
from variables import keep_var as v

def execute():
    while True:
        # --- keepドメイン: 書き込み可能 ---
        # 変更は即座にマスターデータへ反映されます。
        v.keep.status = "RUNNING"

        # --- loop/master/systemドメイン: 読み取り専用（保護あり） ---
        # プロパティを通じて常に「コピー」が返されるため、
        # 以下の操作は実体（マスター）を一切汚染しません。
        v.loop.counter = -999    # 無効（実体は守られる）
        v.master.max_speed = 0   # 無効（実体は守られる）
        
        time.sleep(1.0)

```

---

## 3. 初期化・終了・デバッグ（`0_setup`, `2_teardown`）

**使用する変数:** `master_var`
**特徴:** システムの管理・初期化のための全権限を行使（ただし `system` 領域を除く）。

```python
from variables import master_var as v

def execute():
    # --- loop/keep/masterドメイン: 直接操作可能 ---
    # セットアップ時に必要なパラメータを強制的にセットします。
    v.master.max_speed = 2500
    v.loop.counter = 0

    # --- systemドメイン: 憲法としての保護 ---
    # master_varであっても、systemドメインだけは書き換えがブロックされます。
    v.system.version = "2.0.0" # 実体は1.0.0のまま守られます

```

---

## 重要な補足：書き換えの「無効」について

上記のサンプルで「無効」と記している箇所は、Pythonの文法エラー（例外）を投げることはありませんが、**マスターデータが保持している「真の実体」は1bitも変化しない**ことを意味します。

