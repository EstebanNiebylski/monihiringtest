from django.urls import path
from loan.api.view import LoanApiView, LoanDetail

urlpatterns = [
    path('loan/', LoanApiView.as_view(), name = 'loans'),    
    path('loan/<int:pk>/', LoanDetail.as_view()),
]
