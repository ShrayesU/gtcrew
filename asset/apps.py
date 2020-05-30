from django.apps import AppConfig


class AssetConfig(AppConfig):
    name = 'asset'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Asset'))
