from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_notification_email(address, subject, message):
    # subscribers = list(Subscription.objects.filter(course=pk).values_list('user__email', flat=True))

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[address],
        fail_silently=False,
    )
