from django.db import models

# Fake model for dashboard option
class Dashboard(models.Model):

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboard'
        managed = False # prevent table creation