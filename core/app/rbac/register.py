from django.contrib import admin
from django.http import HttpRequest

from typing import Any

from app.models import (
    Inventory, Product, Warehouse, Transaction, Role, Permission, UserAuthProxyModel
)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1 # number of forms to show
    fields = (
        'name', 'supplier_name', 'supplier_mail', 'quantity', 'price'
    )
    show_change_link = True


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]

    list_display = (
        'name',
        'warehouse',
        'capacity',
        'location',
        'created_at',
    )


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'road', 'city', 'state', 'country', 'capacity')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'product', 'product_name', 'product_quantity', 'supplier_name', 'supply_date',
        'target_inventory', 'target_warehouse'
    )
    readonly_fields = ('product_name', 'product_quantity', 'supplier_name', 'supplier_mail', 'target_inventory', 'target_warehouse', 'supply_date')


class PermissionInline(admin.TabularInline):
    model = Permission
    extra = 1 # number of forms to show
    fields = ('resource', 'level')
    show_change_link = True


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    inlines = [PermissionInline]

    list_display = ('name',)


@admin.register(UserAuthProxyModel)
class UserAuthAdmin(admin.ModelAdmin):

    filter_horizontal = ('roles',)  # allows multi-select in admin

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False