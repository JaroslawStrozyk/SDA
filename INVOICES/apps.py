from django.apps import AppConfig


class InvoicesConfig(AppConfig):
    name = 'INVOICES'

    def ready(self):
        import INVOICES.signals
