from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils import timezone

from app.models.invite import Invite


User = get_user_model()

def activate_invite_login(request, token):
        
    try:
        invite = Invite.objects.get(token=token, status='P')
    except Invite.DoesNotExist: 
        messages.error(request, "Invalid invitation")
        return render(request, 'admin/invite_activation.html')

    if invite.expires_at < timezone.now():  # type: ignore
        invite.status = 'E'
        invite.save(update_fields=['status'])
        messages.error(request, "Invitation expired.")
        return render(request, 'admin/invite_activation.html')

    if request.method == 'POST':
        password = request.POST.get('password')

        if not password: 
            messages.error(request, "Password is requried")
            return render(request, 'admin/invite_activation.html')

        try: 
            with transaction.atomic():
                invite = Invite.objects.select_for_update().get(pk=invite.pk)

                if invite.status != 'P':
                    messages.error(request, "Invitation already used.")
                    return redirect("/login/")
                
                # Create user
                user = User.objects.create(
                    username=invite.email,
                    email=invite.email,
                    is_active=True,
                    is_staff=True,  # if admin access required
                )
                user.set_password(password)
                user.save()

                # Invalidate invite
                invite.status = 'A'
                invite.token = ''
                invite.save(update_fields=["status", "token"])

        except Exception:
            messages.error(request, "Activation failed. Try again.")
            return render(request, 'admin/invite_activation.html')

        login(request, user)
        messages.success(request, "Account activated successfully.")
        return redirect("/")
    
    return redirect("/login/")