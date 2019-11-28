from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('eimi_p/',include("eimidb.urls")),
    path('admin/', admin.site.urls),
]
