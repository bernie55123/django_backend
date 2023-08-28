from django.dispatch import Signal, receiver
from django.db.models.signals import post_save,pre_save
from .models import trade_request
from .send import send_email

# 定義信號
post_result_change = Signal()


@receiver(post_save, sender=trade_request)
def result_change_send_gmail(sender, instance, **kwargs):
    if instance.result is not None:
        send_email(instance)

@receiver(post_save, sender=trade_request)
def trade_send_backend(sender, instance,created, **kwargs):
    if created:
        send_email(instance)  