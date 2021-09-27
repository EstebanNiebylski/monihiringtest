from django.urls import path
from loan.api.view import loan_api_view

urlpatterns = [
    path('loan/', loan_api_view, name = 'loan_api'),    
]
