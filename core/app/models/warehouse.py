from django.db import models


# Model for warehouses
# Visibility: Invisible
class Warehouse(models.Model):

    # Warehouse names must be unique
    name = models.CharField(verbose_name='warehouse_name', max_length=255, blank=False, null=False, unique=True)
    capacity = models.PositiveIntegerField(verbose_name='warehouse_capacity')
    
    # Geolocation of the warehouse
    road = models.CharField(verbose_name='road_location', max_length=255, blank=False, null=False, default='N/A')
    city = models.CharField(verbose_name='city_location', max_length=255, blank=False, null=False, default='Dhaka')
    state = models.CharField(verbose_name='state_location', max_length=255, blank=False, null=False, default='Dhaka')
    country = models.CharField(verbose_name='country_location', max_length=255, blank=False, null=False, default='Bangladesh')

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'        

    def __str__(self) -> str:
        return f'{self.name} {self.road} {self.city} {self.state} {self.country}'
