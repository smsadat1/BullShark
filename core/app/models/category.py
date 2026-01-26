from django.db import models

class Category(models.Model):
    name = models.CharField(verbose_name='category', max_length=255, unique=True)
    description = models.TextField(blank=True)

    # Time records
    created_at = models.DateTimeField(verbose_name='creation time', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='last update', auto_now=True)
    
    class Meta: 
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' 
