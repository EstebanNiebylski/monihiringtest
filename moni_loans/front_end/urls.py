from django.urls import path, include
from front_end.views import index_tmpl, admin_tmpl

urlpatterns = [
    path("", index_tmpl),   
    path("admin/", admin_tmpl),  
]
