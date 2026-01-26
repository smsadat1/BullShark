from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver 

from app.models import History
from app.models import Transaction


@receiver(pre_save, sender=Transaction)
def populate_transaction_field(sender, instance, **kwargs):

    product = instance.product
    instance.product_name = product.name
    instance.product_quantity = product.quantity
    instance.supplier_name = product.supplier_name
    instance.supplier_mail = product.supplier_mail
    instance.target_inventory = product.inventory
    instance.target_warehouse = product.inventory.warehouse


@receiver(post_save, sender=LogEntry)
def sync_history(sender, instance, created, **kwargs):

    # create history logs only when new log is entered
    if not created:
        return
    
    ACTION_MAP = {
        ADDITION : 'ADD',
        CHANGE   : 'UPDATE',
        DELETION : 'DELETE',
    }

    action_type = ACTION_MAP.get(instance.action_flag, 'SYSTEM')    # SYSTEM for everything else

    History.objects.create(
        user=instance.user,
        action=instance.change_message or str(instance),
        action_type=action_type,

        model=instance.content_type.model,
        object_id=instance.object_id,

        details={
            "object_repr": instance.object_repr,
            "change_message": instance.change_message,
            "app_label": instance.content_type.app_label,
        }
    )