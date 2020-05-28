from django.apps import AppConfig


class TeamConfig(AppConfig):
    name = 'team'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Profile'))
