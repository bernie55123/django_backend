from django.dispatch import Signal, receiver
from django.db.models.signals import post_save,pre_save
from .models import decrease_point
from .views import decreasepoint


trust_point_change = Signal()

@receiver(post_save, sender=decrease_point)
def trust_point_decrease(sender, instance,created, **kwargs):
    decreasepoint(sender=instance)