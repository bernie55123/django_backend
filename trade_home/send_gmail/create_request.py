import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from .models import trade_request


@csrf_exempt
def create_requist(request):
    if request.method == "POST":
        id = request.POST.get("email")
        balance = request.POST.get("balance")
        task_name = request.POST.get("name")
        task_cost = request.POST.get("token")
        people_limit = request.POST.get("people")
        point_limit = request.POST.get("point")
        description_limit =request.POST.get("description")
        task_info = request.POST.get("overview")
        task_cover = request.POST.get("task_cover")
        create_trade_request = trade_request(id=id ,balance=balance ,task_name=task_name ,task_cost=task_cost ,people_limit=people_limit,point_limit=point_limit,description_limit=description_limit,task_info=task_info ,result=None)
        create_trade_request.save()
        
        response_data = {'message': 'Task created successfully'}

        response = JsonResponse(response_data)
        response['Access-Control-Allow-Origin'] =  '*'  # 允許所有域名的跨域請求
        response['Access-Control-Allow-Methods'] = 'POST'  # 允許的 HTTP 方法
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'  # 允許的 HTTP 頭

        return response

