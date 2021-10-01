from django.urls import path
from users.api.view import RequesterApiView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('requesters/', RequesterApiView.as_view(), name = 'Requesters'),     
    path('login/', obtain_auth_token, name = 'obtain_token'),
]