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
        tack_info = request.POST.get("overview")
        create_trade_request = trade_request(id=id ,balance=balance ,task_name=task_name ,task_cost=task_cost ,tack_info=tack_info ,result=None)
        create_trade_request.save()
        
        response_data = {'message': 'Task created successfully'}

        response = JsonResponse(response_data)
        response['Access-Control-Allow-Origin'] =  '*'  # 允許所有域名的跨域請求
        response['Access-Control-Allow-Methods'] = 'POST'  # 允許的 HTTP 方法
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'  # 允許的 HTTP 頭

        return response

