from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from loan.models import Loan
from loan.api.serializers import LoanSerializer

@api_view(['GET', 'POST'])
def loan_api_view(request, id):
    
    if request.method == 'GET':
        all_loans = Loan.objects.all()
        loan_serializer = LoanSerializer(all_loans, many=True)                  
        return Response(data=loan_serializer.data)
    elif request.method == 'POST':
        pass
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
