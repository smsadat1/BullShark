import uuid
from django.db import models

from app.services.mail import send_invitation_mail
from config.settings import AUTH_USER_MODEL

# Admin only 
class Invite(models.Model):

    INVITE_STATUS = (
        ('P', 'PENDING'),
        ('A', 'ACCEPTED'),
        ('E', 'EXPIRED'),
        ('R', 'REVOKED'),
    )

    email = models.EmailField(verbose_name='Invited mail', unique=True)
    role = models.ForeignKey('Role', on_delete=models.PROTECT, verbose_name='Given role')
    warehouses = models.ManyToManyField('WareHouse', blank=True, verbose_name='Enrolled Warehouse')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    status = models.CharField(max_length=1, choices=INVITE_STATUS, default='P')
    invited_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sent_invites", verbose_name='Invited by')

    # Time records
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Invited at')
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)

    # Email status
    email_sent = models.BooleanField(default=False)
    email_error = models.TextField(blank=True, null=True)

    class Meta: 
        verbose_name = 'Invite'
        verbose_name_plural = 'Invites'

    