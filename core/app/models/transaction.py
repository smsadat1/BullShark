from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from config import settings

# Model to audit transaction history
# Dependency: Product, Inventory, Warehouse
# Visibility: visible
class Transaction(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    # These fields are copied from Product at the time of transaction
    product_name = models.CharField(max_length=255, blank=False, null=False)
    product_quantity = models.PositiveBigIntegerField()
    supplier_name = models.CharField(max_length=255, blank=False, null=False)
    supplier_mail = models.CharField(max_length=255, blank=False, null=False)

    # Supply info 
    supply_date = models.DateTimeField(auto_now_add=True)

    # Inventory and warehouse at the time of transaction
    target_inventory = models.ForeignKey('Inventory', on_delete=models.PROTECT)
    target_warehouse = models.ForeignKey('Warehouse', on_delete=models.PROTECT)



