import json,base64
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from pathlib import Path
from .models import trade_request
import datetime,re


defalut_type=["環境清理","照顧寵物","照護","課業輔導","行政支援"]

@csrf_exempt
def create_request(request):
    if request.method == "POST":
        create_trade_request = trade_request()
        req = request.POST.dict()
        create_trade_request.obj_user = request.POST.get("email")
        create_trade_request.balance = request.POST.get("balance")
        create_trade_request.task_name = request.POST.get("name")
        create_trade_request.task_cost = request.POST.get("token")
        create_trade_request.max_people = request.POST.get("people")
        create_trade_request.point_limit = request.POST.get("point")
        create_trade_request.description_limit =request.POST.get("description")
        create_trade_request.task_info = request.POST.get("overview")
        create_trade_request.thumbnail,create_trade_request.img = cover_decode(req)
        if create_trade_request.task_name not in defalut_type:
            create_trade_request.result = None
            create_trade_request.save()
        else:
            create_trade_request.result = True
            create_trade_request.save()
            create_trade_request.delete()
        
        response_data = {'message': 'Task created successfully'}

        response = JsonResponse(response_data)
        response['Access-Control-Allow-Origin'] =  '*'  # 允許所有域名的跨域請求
        response['Access-Control-Allow-Methods'] = 'POST'  # 允許的 HTTP 方法
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'  # 允許的 HTTP 頭

        return response

def cover_decode(req):

    img = req["cover"]
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
    return cover_path,img