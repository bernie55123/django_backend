from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import trade_request,trust_point,Profile
import json


@csrf_exempt
def get_data(request):
    email = request.POST.get("email")
    TRU = trade_request.objects.get(obj_user=email)
    response = HttpResponse()
    data = json.dumps({
        "max_people" : TRU.max_people,
        "now_people" : TRU.now_people,
        "point_limit" : TRU.point_limit,
        "task_name" : TRU.task_name,
        "task_cost" : TRU.task_cost,
        "thumbnail" : TRU.thumbnail,
        "description_limit" : json.loads(TRU.description_limit)
    })
    response.write(data)
    return response

#扣除信用積分
@csrf_exempt
def decreasepoint(sender):
    try:
        trust_point_record = Profile.objects.get(obj_user=sender.obj_user)
        trust_point_record.trust_point -= sender.decrease_point
        if trust_point_record.trust_point<0:
                trust_point_record.trust_point = 0
        trust_point_record.save()
    except Profile.DoesNotExist:
        pass

#新增信用積分
def increasepoint(sender):
    try:
        trust_point_record = Profile.objects.get(obj_user=sender.obj_user)
        if trust_point_record.trust_point+sender.increase_point<100:
            trust_point_record.trust_point += sender.increase_point
        trust_point_record.save()
    except Profile.DoesNotExist:
        pass

#取得信用積分
@csrf_exempt
def get_trust_point(request):
    email = request.POST.get("email")
    obj_user = User.objects.filter(email = email).get()
    TRU = trust_point.objects.get(obj_user=obj_user)
    response = HttpResponse()
    data = json.loads(str(TRU.trust_point))
    response.write(data)
    return response

