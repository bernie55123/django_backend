from django.contrib import admin
from .models import trade_request,Profile,trust_point

# Register your models here.
admin.site.register(trade_request)
admin.site.register(Profile)
admin.site.register(trust_point)