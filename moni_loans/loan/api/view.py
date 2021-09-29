import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from loan.models import Loan
from loan.api.serializers import LoanInfoSerializer, LoanCreatorSerializer
from users.api.serializers import RequesterSerializer
from users.models import Requester
from moni_loans.settings import MONI_API_KEY


def loan_validator(dni):
    """
    Given a 'dni', send a request to an endpoint of mony
    to know if aprove or deny the loan request
    :return:
    """
    api_key = MONI_API_KEY    
    headers = {'credential': api_key}    
    url = 'https://api.moni.com.ar/api/v4/scoring/pre-score/'    
    try:
        response = requests.get(url + dni, headers=headers)        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()            
            if not data["has_error"]:                                
                if data['status'] == 'approve':
                    return 'OK'
                else:
                    # 'status' = rejected
                    return 'NO'
            else:
                raise Exception("error when trying to validate the dni.")
    except Exception as error:
        raise error
    return 'OK'


class LoanApiView(APIView):
    
    def get(self, request):
        all_loans = Loan.objects.all()
        loan_serializer = LoanInfoSerializer(all_loans, many=True)                  
        return Response(data=loan_serializer.data)
        
    def post(self, request):
        """
        Create an instance of a loan and, if the user not exist, create a user too

        request.data expected:
        {
            "amount": <float>,            
            "requester_info": {
                "email": <String>,
                "dni": <String> of length 8,
                "lastname": <String>,
                "name": <String>,
                "gender": Enum('M', 'F', 'X')
            }
        }
        :return: loan id and status
        """        
        # If user not exist, create it first and then the loan        
        requester_info = request.data.get('requester_info', None)
        requester_id = None
        if requester_info is not None: 
            try:
                requester_id = Requester.objects.get(dni=request.data['requester_info']['dni'])
            except Requester.DoesNotExist:                
                # Create user
                requester_serializer = RequesterSerializer(data=requester_info)
                if requester_serializer.is_valid():
                    requester_id = requester_serializer.save()                    
                else:
                    return Response(requester_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Missing param": "requester_info"}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data                
        data['requester'] = str(requester_id.id)
        loan_serializer = LoanCreatorSerializer(data=data)  
        dni = request.data['requester_info']['dni']                                                                                 
        request.data['state'] = loan_validator(dni)
        if loan_serializer.is_valid():                   
            new_loan = loan_serializer.save() 
            return Response(data=loan_serializer.data, status=status.HTTP_201_CREATED)            
        else:
            return Response(loan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
