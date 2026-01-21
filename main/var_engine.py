import copy

class VariableDomain:
    """loop, keep, master, systemといった特定の領域を管理するクラス"""
    def __init__(self, data_dict):
        # 初期化時にもディープコピーを適用し、参照の共有を完全に断ち切ります
        for key, value in data_dict.items():
            setattr(self, key, copy.deepcopy(value))

    def update_from(self, other_domain):
        """他のドメインから値をディープコピーして同期する"""
        for key, value in other_domain.__dict__.items():
            setattr(self, key, copy.deepcopy(value))

class VariableWorkspace:
    """Loopフェーズ用の作業机、またはマスター実体（master_var）を表すクラス"""
    def __init__(self, data):
        self.loop = VariableDomain(data.get('loop', {}))
        self.keep = VariableDomain(data.get('keep', {}))
        self.master = VariableDomain(data.get('master', {}))
        # system領域は内部の実体として秘匿し、直接の書き換えを防御します
        self._system_actual = VariableDomain(data.get('system', {}))

    @property
    def system(self):
        """
        system領域へのアクセスインターフェースです。
        master_varからアクセスした場合でも常にディープコピーを返すため、
        戻り値の属性を書き換えても実体には影響を与えません。
        """
        return copy.deepcopy(self._system_actual)

    def sync_from(self, source_master):
        """【Snapshot】マスターから現在の全データをコピーしてくる"""
        self.loop.update_from(source_master.loop)
        self.keep.update_from(source_master.keep)
        self.master.update_from(source_master.master)
        # systemも同期対象に含めますが、実体（_system_actual）に対して同期します
        self._system_actual.update_from(source_master._system_actual)

    def commit_to_master(self, target_master):
        """【Commit】自分の『loop領域』だけをマスターに書き戻す"""
        # loop以外の領域（keep, master, system）はコミット対象外となり、保護されます
        target_master.loop.update_from(self.loop)

class KeepWorkspace:
    """Keepフェーズ用の、保護されたアクセス窓口クラス"""
    def __init__(self, master_workspace):
        # keep領域はマスターへの直接参照（リアルタイム更新用）
        self.keep = master_workspace.keep
        self._master = master_workspace
    
    @property
    def loop(self):
        # loop領域へのアクセスには常にコピーを返し、書き換えを無効化します
        return copy.deepcopy(self._master.loop)

    @property
    def master(self):
        # master領域もkeep側からは読み取り専用として扱います
        return copy.deepcopy(self._master.master)

    @property
    def system(self):
        # system領域も同様に読み取り専用です
        return copy.deepcopy(self._master.system)