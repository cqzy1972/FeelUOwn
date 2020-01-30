"""
本地收藏管理
~~~~~~~~~~~~~
"""
import base64

from fuocore.utils import elfhash
from feeluown.widgets.collections import CollectionsModel
from feeluown.collection import CollectionType


class CollectionUiManager:
    def __init__(self, app):
        self._app = app
        self.model = CollectionsModel(app)
        self._id_coll_mapping = {}

    def get(self, identifier):
        return self._id_coll_mapping.get(identifier, None)

    def get_coll_id(self, coll):
        # TODO: 目前还没想好 collection identifier 计算方法，故添加这个函数
        # 现在把 fpath 当作 identifier 使用，但对外透明
        return elfhash(base64.b64encode(bytes(coll.fpath, 'utf-8')))

    def add(self, collection):
        coll_id = self.get_coll_id(collection)
        self._id_coll_mapping[coll_id] = collection
        self.model.add(collection)

    def clear(self):
        self._id_coll_mapping.clear()
        self.model.clear()

    def initialize(self):
        self._scan()

    def refresh(self):
        """重新加载本地收藏列表"""
        self.model.clear()
        self._scan()

    def _scan(self):
        colls = []
        song_coll = None
        album_coll = None
        for coll in self._app.coll_mgr.scan():
            if coll.type == CollectionType.sys_song:
                song_coll = coll
                continue
            if coll.type == CollectionType.sys_album:
                album_coll = coll
                continue
            colls.append(coll)
        colls.insert(0, album_coll)
        colls.insert(0, song_coll)
        for coll in colls:
            self.add(coll)
