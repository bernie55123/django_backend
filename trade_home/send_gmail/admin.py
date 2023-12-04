from django.contrib import admin
from .models import trade_request,Profile,trust_point

# Register your models here.

class trade_request_admin(admin.ModelAdmin):
    list_display = ("id","obj_user","task_name")
admin.site.register(trade_request,trade_request_admin)

class Profile_admin(admin.ModelAdmin):
    list_display = ("id","obj_user","balance","trust_point")
admin.site.register(Profile,Profile_admin)

class trust_point_admin(admin.ModelAdmin):
    list_display = ("id","obj_user")
admin.site.register(trust_point,trust_point_admin)