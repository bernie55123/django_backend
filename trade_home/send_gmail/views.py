from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import trade_request,trust_point,Profile
import json,requests


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
        if trust_point_record.trust_point <= 0:
                trust_point_record.trust_point = 0
        trust_point_record.save()
    except Profile.DoesNotExist:
        pass

#新增信用積分
def increasepoint(sender):
    try:
        trust_point_record = Profile.objects.get(obj_user=sender.obj_user)
        print(trust_point_record.trust_point)
        if trust_point_record.trust_point+sender.increase_point<=100:
            trust_point_record.trust_point += sender.increase_point
        else:
            trust_point_record.trust_point = 100
        trust_point_record.save()
        print(sender.increase_point)
        print(trust_point_record.trust_point)
    except Profile.DoesNotExist:
        pass

#取得信用積分
@csrf_exempt
def get_trust_point(request):
    email = request.POST.get("email")
    obj_user = User.objects.filter(email = email).get()
    TRU = Profile.objects.get(obj_user=obj_user)
    response = HttpResponse()
    data = json.loads(str(TRU.trust_point))
    response.write(data)
    return response


#取得可發布任務數量
@csrf_exempt
def get_number_of_task(request):
    email = request.POST.get('email')
    obj_user = User.objects.filter(email=email).get()
    user_profile = Profile.objects.filter(obj_user=obj_user).get()
    response = HttpResponse()
    data = json.dumps({
        "number_of_task": user_profile.number_of_task,
        "number_of_task_max": user_profile.number_of_task_max,
    })
    response.write(data)
    return response

#任務結束回復可發布任務數量
@csrf_exempt
def reply_number_of_task(request):
    email = request.POST.get('email')
    obj_user = User.objects.filter(email=email).get()
    user_profile = Profile.objects.filter(obj_user=obj_user).get()
    user_profile.number_of_task = user_profile.number_of_task-1
    Profile.objects.filter(obj_user=obj_user.id).update(number_of_task=user_profile.number_of_task)
    response = HttpResponse()
    response.write("The number of task is reply!")
    return response