from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver 

from app.models import History, Invite, Transaction
from app.services.mail import send_invitation_mail

@receiver(pre_save, sender=Transaction)
def populate_transaction_field(sender, instance, **kwargs):

    product = instance.product
    instance.product_name = product.name
    instance.product_quantity = product.quantity
    instance.supplier_name = product.supplier_name
    instance.supplier_mail = product.supplier_mail
    instance.target_inventory = product.inventory
    instance.target_warehouse = product.inventory.warehouse


# Transaction logging

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


# Mail service 

@receiver(post_save, sender=Invite)
def send_invite_email(sender, instance, created, **kwargs):

    if created and instance.status == 'P':
        # Delay until transaction is committed
        transaction.on_commit(lambda: __send_email(instance.pk))

def __send_email(invite_id):

    invite = Invite.objects.get(pk=invite_id)

    try: 
        send_invitation_mail(
            email=invite.email,
            role=invite.role,
            warehouse=", ".join([w.name for w in invite.warehouses.all()]),
            expires_at=str(invite.expires_at),
        )

        invite.email_sent = True 
        invite.email_error = None 

    except Exception as e: 
        invite.email_sent = False
        invite.email_error = str(e)

    invite.save(update_fields=["email_sent", "email_error"])

