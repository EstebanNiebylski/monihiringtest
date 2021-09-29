from django.urls import path
from users.api.view import RequesterApiView

urlpatterns = [
    path('requesters/', RequesterApiView.as_view(), name = 'Requesters'), 
    # Implementar login
]