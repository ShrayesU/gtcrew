from django.apps import AppConfig


class GTCrewConfig(AppConfig):
    name = 'gtcrew'
    verbose_name = 'GT Crew'

    def ready(self):
        import gtcrew.signals
