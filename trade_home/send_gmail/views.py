from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import trade_request
import json


@csrf_exempt
def get_data(request):
    email = request.POST.get("email")
    TRU = trade_request.objects.get(id = email)
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


