from django.contrib.auth.models import AbstractUser
from django.db import models

# Model for roles
# Visibility: Invisible
class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

# Model for permissions
# Permission has 4 level: R, C, E, D || With 3 layers: Warehouse, Inventory, Product
# Visibility: Invisible
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