from django.dispatch import Signal, receiver
from django.db.models.signals import post_save,pre_save
from .models import trade_request,trust_point
from .send import send_email
from .views import decreasepoint,increasepoint

# 定義信號

jump = None

requests_type_is_true = Signal()
@receiver(pre_save, sender=trade_request)
def requests_type_is_true(sender,instance,**kwargs):
    defalut_type=["環境清理","照顧寵物","照護","課業輔導","行政支援"]
    if instance.task_name in defalut_type:
        jump = True
        send_email(instance,jump)

post_result_change = Signal()
@receiver(post_save, sender=trade_request)
def result_change_send_gmail(sender, instance,created, **kwargs):
    if created:
        send_email(instance,jump) 
    elif instance.result is not None:
        send_email(instance,jump)

trust_point_change_ = Signal()

@receiver(post_save, sender=trust_point)
def trust_point_change(sender, instance,created, **kwargs):
    decreasepoint(sender=instance)
    increasepoint(sender=instance)

