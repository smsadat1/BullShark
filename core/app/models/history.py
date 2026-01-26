from django.db import models

from config import settings

class History(models.Model):

    ACTION_TYPES = [
        ('ADD', 'Add'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('IMPORT', 'Import'),
        ('SYSTEM', 'System'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=512)
    action_type = models.CharField(max_length=10, choices=ACTION_TYPES)
    
    model = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50)
    details = models.JSONField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
