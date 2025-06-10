from django.core.mail import send_mail
from django.conf import settings

send_mail(
    subject='Test Email',
    message='This is a test.',
    from_email=settings.EMAIL_FROM_EMAIL,
    recipient_list=['epicmmmoss@gmail.com'],
    fail_silently=False,
)

print("EMAIL_HOST is:", settings.EMAIL_HOST)
