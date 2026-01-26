from django.apps import AppConfig


class appConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'BullShark Inventory Manager'

    def ready(self):
        import app.rbac     # Make sure to register in admin dashboard 
        import app.rbac.signals

