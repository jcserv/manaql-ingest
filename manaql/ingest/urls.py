from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def hello(request):
    return HttpResponse("Hello, Fly!")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", hello, name="hello"),
]
