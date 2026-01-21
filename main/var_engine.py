import copy

class VariableDomain:
    """loopやkeepといった特定の領域を管理するクラス"""
    def __init__(self, data_dict):
        # 初期化時にもディープコピーを適用し、参照の共有を完全に断ち切ります
        for key, value in data_dict.items():
            setattr(self, key, copy.deepcopy(value))

    def update_from(self, other_domain):
        """他のドメインから値をディープコピーして同期する"""
        for key, value in other_domain.__dict__.items():
            setattr(self, key, copy.deepcopy(value))

class VariableWorkspace:
    """Loop用やKeep用などの『作業机』を表すクラス"""
    def __init__(self, data):
        self.loop = VariableDomain(data.get('loop', {}))
        self.keep = VariableDomain(data.get('keep', {}))

    def sync_from(self, source_master):
        """【Snapshot】マスターから現在の全データをコピーしてくる"""
        self.loop.update_from(source_master.loop)
        self.keep.update_from(source_master.keep)

    def commit_to_master(self, target_master):
        """【Commit】自分の『loop領域』だけをマスターに書き戻す"""
        target_master.loop.update_from(self.loop)