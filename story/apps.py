from django.apps import AppConfig


class StoryConfig(AppConfig):
    name = 'story'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Story'))
