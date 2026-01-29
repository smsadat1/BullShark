from django.contrib import admin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import path, reverse


from typing import Any

from app.models import (
    Category, Dashboard, Inventory, Invite, Product, Warehouse, Transaction, History, Role, Permission, Profile, UserAuthProxyModel
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'updated_at',
    )


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
# Wrapped around fake class to make the redirect work    
    def changelist_view(self, request, extra_context=None): # type: ignore
        return redirect(reverse('admin:index'))

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


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):


    def get_warehouses(self, obj):
        return ", ".join([w.name for w in obj.warehouses.all()])

    list_display = (
        'email',
        'role',
        'get_warehouses',
        'status',
        'invited_by',
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

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_view_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return True


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

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_view_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return True
    
    list_display = (
        'user',
        'action_type',
        'time',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(self.profile_view), name='profile'),
        ]

        return custom_urls + urls


    def profile_view(self, request):
        user  = request.user
        password_form = AdminPasswordChangeForm(user, request.POST or None)
        password_changed = False

        if request.method == 'POST' and password_form.is_valid():
            password_form.save()

            # keep logged in after changfe
            update_session_auth_hash(request, user)
            password_changed = True 

        context = {
            **self.admin_site.each_context(request),
            'user': user,
            'password_form': password_form,
            'password_changed': password_changed,
            'title': 'Your Profile',
        }   

        return render(request, 'admin/profile.html', context)     
