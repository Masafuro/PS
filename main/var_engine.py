import copy

class VariableDomain:
    """loopやkeepといった特定の領域を管理するクラス"""
    def __init__(self, data_dict):
        for key, value in data_dict.items():
            setattr(self, key, copy.deepcopy(value))

    def update_from(self, other_domain):
        """他のドメインから値をディープコピーして同期する"""
        for key, value in other_domain.__dict__.items():
            setattr(self, key, copy.deepcopy(value))

class VariableWorkspace:
    """Loopフェーズ用の作業机、またはマスター実体を表すクラス"""
    def __init__(self, data):
        self.loop = VariableDomain(data.get('loop', {}))
        self.keep = VariableDomain(data.get('keep', {}))

    def sync_from(self, source_master):
        self.loop.update_from(source_master.loop)
        self.keep.update_from(source_master.keep)

    def commit_to_master(self, target_master):
        target_master.loop.update_from(self.loop)

class KeepWorkspace:
    """Keepフェーズ用の、保護されたアクセス窓口クラス"""
    def __init__(self, master_workspace):
        # keep領域はマスターへの直接参照（リアルタイム更新用）
        self.keep = master_workspace.keep
        # マスター実体を内部に保持
        self._master = master_workspace
    
    @property
    def loop(self):
        # loop領域へのアクセスには常にコピーを返す
        # これにより、書き換えてもマスターは汚染されません
        return copy.deepcopy(self._master.loop)