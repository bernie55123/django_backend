from django.contrib import admin
from .models import trade_request,id_info

# Register your models here.
admin.site.register(trade_request)
admin.site.register(id_info)
