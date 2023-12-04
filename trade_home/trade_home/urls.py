"""
URL configuration for trade_home project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView
from send_gmail.create_request import create_request
from send_gmail.views import get_data,get_trust_point,get_number_of_task,reply_number_of_task



urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_request', create_request),
    path('get_trust_point',get_trust_point),
    path('get_data',get_data),
    path('get_number_of_task',get_number_of_task),
    path('reply_number_of_task',reply_number_of_task),

]

