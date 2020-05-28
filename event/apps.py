from django.apps import AppConfig


class EventConfig(AppConfig):
    name = 'event'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Event'))
        registry.register(self.get_model('Result'))
