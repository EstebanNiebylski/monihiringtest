from django.urls import path
from user.api.view import user_list, get_user_from_dni

urlpatterns = [
    path('user/', user_list, name = 'user_list'),
    path('user/<dni>', get_user_from_dni, name = 'user'),
]
