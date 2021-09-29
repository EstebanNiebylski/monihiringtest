from django.urls import path
from loan.api.view import LoanApiView

urlpatterns = [
    path('loan/', LoanApiView.as_view(), name = 'loan_list'),    
]
