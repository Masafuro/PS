# 共有変数アクセス 実装サンプル集

本フレームワークにおける、各実行フェーズごとの共有変数へのアクセスと、書き換え保護機能の挙動に関する具体例をまとめます。

## 1. 同期制御フェーズ（`1_loop`）

**使用する変数:** `loop_var`
**特徴:** 制御ロジックの整合性を保つための「スナップショット・コミット」方式。

```python
from variables import loop_var as v

def execute():
    # --- loop領域: 所有権あり ---
    # 読み書き可能。変更はサイクル終了時にマスターデータへ反映されます。
    v.loop.counter += 1

    # --- keep/master/system領域: 読み取り専用（スナップショット） ---
    # 参照される値はサイクル開始時に固定されたものです。
    if v.keep.status == "ACTIVE":
        # 書き換えてもエラーにはなりませんが、このサイクル内の一時的なメモとなり、
        # 他のフェーズやマスターデータには一切反映されません。
        v.master.max_speed = 0  # これはマスターを汚染しません
        
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
        # --- keep領域: 所有権あり ---
        # 読み書き可能。変更は即座にマスターデータへ反映されます。
        v.keep.status = "RUNNING"

        # --- loop/master/system領域: 読み取り専用（保護あり） ---
        # プロパティを通じて常に「ディープコピー（複製）」が返されます。
        # 属性を書き換えても「使い捨てのコピー」を汚すだけで終わります。
        v.loop.counter = -999    # 無効（実体は守られる）
        v.master.max_speed = 0   # 無効（実体は守られる）
        v.system.version = "X"   # 無効（実体は守られる）
        
        time.sleep(1.0)

```

---

## 3. 初期化・終了・デバッグ（`0_setup`, `2_teardown`）

**使用する変数:** `master_var`
**特徴:** システムの管理・初期化のための全権限を行使（ただし `system` 領域を除く）。

```python
from variables import master_var as v

def execute():
    # --- loop/keep/master領域: 直接操作可能 ---
    # マスターデータの実体を直接読み書きし、初期状態を構築します。
    v.master.max_speed = 2500
    v.loop.counter = 0
    v.keep.status = "Standby"

    # --- system領域: 憲法としての保護 ---
    # master_varであっても、systemドメインへのアクセスは常にコピーを介します。
    # したがって、ここでも書き換えは実体に届きません。
    v.system.version = "2.0.0" # 無効（実体は1.0.0のまま守られる）

```

---

## 重要な補足：書き換えの「無効」について

上記のサンプルで「無効」と記している箇所は、Pythonの文法エラー（例外）を投げることはありませんが、**マスターデータが保持している「真の実体」は1bitも変化しない**ことを意味します。

これにより、以下のメリットが得られます：

* **ロジックの安全性**: 誤って他領域を書き換えるコードを書いても、システムの核となるデータは破壊されません。
* **デバッグの容易性**: 他のフェーズや `2_teardown` で `master_var` を通じて値を確認すれば、不正な書き込みがブロックされたことを容易に検証できます。

