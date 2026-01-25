from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# model: visible

class Transaction(models.Model):

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

@receiver(pre_save, sender=Transaction)
def populate_transaction_field(sender, instance, **kwargs):

    product = instance.product
    instance.product_name = product.name
    instance.product_quantity = product.quantity
    instance.supplier_name = product.supplier_name
    instance.supplier_mail = product.supplier_mail
    instance.target_inventory = product.inventory
    instance.target_warehouse = product.inventory.warehouse


