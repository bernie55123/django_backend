from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.dispatch import receiver
from .models import trust_point,matchmaking,decrease_point


# Create your views here.

#扣除信用積分

@csrf_exempt
def decreasepoint(sender):
    try:
        trust_point_record = trust_point.objects.get(id=sender.id)
        trust_point_record.trust_point -= sender.decrease_point
        trust_point_record.save()
        decrease_point.objects.filter(id=sender.id).delete()
    except trust_point.DoesNotExist:
        pass