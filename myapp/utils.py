import threading
from django.core.mail import send_mail
from django.conf import settings
            
def send_notification_email(user, message, link=None):
    subject = "🔔 You have a new notification on DevMate"
    body = f"{message}\n\nCheck it out here: {link or 'https://www.devmate.space/notification/'}"
    
    def send_async():
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [user.user.email],
            fail_silently=True,
        )
        
    threading.Thread(target=send_async).start()
    