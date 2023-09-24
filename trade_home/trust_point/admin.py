from django.contrib import admin
from .models import trust_point,matchmaking,decrease_point

# Register your models here.
admin.site.register(trust_point)
admin.site.register(matchmaking)
admin.site.register(decrease_point)