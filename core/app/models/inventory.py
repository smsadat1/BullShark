from django.db import models


# visibility: Invisible
class Product(models.Model):

    name = models.CharField(verbose_name='product_name', max_length=255, blank=False, unique=False, null=False)
    supplier_name = models.CharField(verbose_name='product_supplier', max_length=255, blank=False, unique=False, null=False)
    supplier_mail = models.CharField(verbose_name='product_supplier_mail', max_length=255, blank=False, unique=False, null=False)
    quantity = models.PositiveIntegerField(verbose_name='product_quantity')
    sku = models.CharField(verbose_name='product_sku', max_length=255, unique=True, null=False, blank=False)
    price = models.DecimalField(verbose_name='product_price', max_digits=10, decimal_places=2, blank=False, null=False)

    # One inventory can have many product but a product must belong to a single inventory
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE, related_name="products")

    def __str__(self) -> str:
        return self.name
    

# visibility: Visible
# dependency: ProductModel
class Inventory(models.Model):

    name = models.CharField(verbose_name='inventory_name', max_length=255, blank=False, unique=False, null=False)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(verbose_name='inventory_capacity')

    # Location in warehouse
    location = models.CharField(verbose_name='inventory_location', max_length=50)

    # Time records
    created_at = models.DateTimeField(verbose_name='inventory_creation_time', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='inventory_last_update_time', auto_now=True)

    class Meta:

        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'

    def __str__(self) -> str:
        return f'{self.name} {self.created_at} {self.updated_at} {self.capacity} {self.location}'