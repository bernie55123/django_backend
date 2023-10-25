from django.dispatch import Signal, receiver
from django.db.models.signals import post_save,pre_save
from .models import trade_request,trust_point
from .send import send_email
from .views import decreasepoint,increasepoint

# 定義信號
post_result_change = Signal()


@receiver(post_save, sender=trade_request)
def result_change_send_gmail(sender, instance,created, **kwargs):
    if created:
        send_email(instance) 
    elif instance.result is not None:
        send_email(instance)

trust_point_change_ = Signal()

@receiver(post_save, sender=trust_point)
def trust_point_change(sender, instance,created, **kwargs):
    decreasepoint(sender=instance)
    increasepoint(sender=instance)

