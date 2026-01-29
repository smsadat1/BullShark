from django.db import models

class Profile(models.Model):

    class Meta: 
        verbose_name = "Profile"
        verbose_name_plural = "Profile"
        managed = False     # No DB table
