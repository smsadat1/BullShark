from django.http import HttpResponse
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER

def send_invitation_mail(
    email: str, 
    role: str, 
    warehouse: str, 
    expires_at: str,
):
    context = {}

    link = "http://127.0.0.1/not_implemented"
    message = f"""
    You are enrolled as {role} in {warehouse} warehouse.
    Click the following link to verify registration.   
    {link} 
    It'll expire by {expires_at}
    """

    subject = "Invitation mail by Bullshark admin"

    if email and subject and message:
        try:
            send_mail(subject, message, EMAIL_HOST_USER, [email])
            context['result'] = 'Email sent successfully'
        except Exception as e: 
            context['result'] = f'Error sending email: {e}'
        
    else:
        context['result'] = 'All fields are required'
    
