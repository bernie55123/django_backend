import json,base64
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from pathlib import Path
from .models import trade_request
import datetime,re


@csrf_exempt
def create_request(request):
    if request.method == "POST":
        req = request.POST.dict()
        id = request.POST.get("email")
        balance = request.POST.get("balance")
        task_name = request.POST.get("name")
        task_cost = request.POST.get("token")
        max_people = request.POST.get("people")
        point_limit = request.POST.get("point")
        description_limit =request.POST.get("description")
        task_info = request.POST.get("overview")
        thumbnail = cover_decode(req)
        create_trade_request = trade_request(id=id ,balance=balance ,task_name=task_name ,task_cost=task_cost ,max_people=max_people,point_limit=point_limit,description_limit=description_limit,task_info=task_info,thumbnail=thumbnail,result=None)
        create_trade_request.save()
        
        response_data = {'message': 'Task created successfully'}

        response = JsonResponse(response_data)
        response['Access-Control-Allow-Origin'] =  '*'  # 允許所有域名的跨域請求
        response['Access-Control-Allow-Methods'] = 'POST'  # 允許的 HTTP 方法
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'  # 允許的 HTTP 頭

        return response

def cover_decode(req):

    if "data:image/png;base64," in req["cover"]:
        req["cover"] = req["cover"].replace("data:image/png;base64,", "")
    else:
        req["cover"] = req["cover"].replace("data:image/jpeg;base64,", "")

    time = datetime.datetime.now()
    data = req["email"] + str(time)
    new_data = re.sub(r'[^\w-]', '', data)

    file_content = base64.b64decode(req["cover"])

    PATH_COVER = settings.STATICFILES_DIRS[0] + "/tasks/" + new_data + "/cover"
    path_dir_cover = Path(PATH_COVER)
    path_dir_cover.mkdir(parents = True, exist_ok = True)
    with open(PATH_COVER + "/cover.png","wb") as f:
        f.write(file_content)
    cover_path = settings.STATIC_URL + new_data + "/tasks/" + new_data + "/cover/cover.png"
    return cover_path