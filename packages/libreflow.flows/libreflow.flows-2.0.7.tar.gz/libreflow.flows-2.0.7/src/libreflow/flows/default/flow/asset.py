from kabaret import flow
from libreflow.baseflow.asset import (
    Asset               as BaseAsset,
    AssetFamily         as BaseAssetFamily,
    AssetType           as BaseAssetType,
    AssetTypeCollection as BaseAssetTypeCollection,
    AssetCollection
)

from .task import Tasks


class Asset(BaseAsset):
    
    tasks = flow.Child(Tasks)

    def ensure_tasks(self):
        """
        Creates the tasks of this asset based on the default
        tasks created with a template named `asset`, skipping
        any existing task.
        """
        default_tasks = self.tasks.get_default_tasks()

        for dt in default_tasks:
            if not self.tasks.has_mapped_name(dt.name()) and not dt.optional.get():
                t = self.tasks.add(dt.name())
                t.enabled.set(dt.enabled.get())
        
        self.tasks.touch()


class Assets(AssetCollection):

    def add(self, name, object_type=None):
        a = super(Assets, self).add(name, object_type)
        a.ensure_tasks()
        
        return a


class AssetFamily(BaseAssetFamily):
    
    assets = flow.Child(Assets).ui(expanded=True)


class AssetType(BaseAssetType):
    pass


class AssetTypeCollection(BaseAssetTypeCollection):

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(
                path_format='{asset_type}/{asset_family}/{asset}/{task}/{file_mapped_name}/{revision}/{file_base_name}'
            )
