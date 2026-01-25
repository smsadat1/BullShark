from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Permission(models.Model):
    resource = models.CharField(
        max_length=50, choices=[
            ('Warehouse', 'Warehouse'), ('Inventory', 'Inventory'), ('Product', 'Product')
        ]
    )
    level = models.CharField(
        max_length=1, choices=[('R', 'Read'), ('C', 'Create'), ('E', 'Edit'), ('D', 'Delete')]
    )
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='permissions')


class User(AbstractUser):
    # User's role
    role = models.ManyToManyField(Role, related_name='users')


class UserAuthProxyModel(User):

    class Meta:
        proxy = True 
        app_label = 'auth' # to move under auths
        verbose_name = 'User'
        verbose_name_plural = 'Users'