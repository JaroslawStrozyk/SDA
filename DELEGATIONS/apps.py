from django.apps import AppConfig


class DelegationsConfig(AppConfig):
    name = 'DELEGATIONS'

    def ready(self):
        import DELEGATIONS.signals
