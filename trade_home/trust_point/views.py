from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import trust_point,matchmaking,decrease_point
import json


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
@csrf_exempt
def get_trust_point(self,req):
    obj_user = User.objects.get(email=req["email"])
    TRU = trust_point.objects.get(id = obj_user)
    response = HttpResponse()
    data = json.loads(TRU.trust_point)
    response.write(data)
    return response