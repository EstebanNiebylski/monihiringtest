import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from loan.models import Loan
from loan.api.serializers import LoanInfoSerializer, LoanCreatorSerializer, LoanModifySerializer
from users.api.serializers import RequesterSerializer
from users.models import Requester
from moni_loans.settings import MONI_API_KEY
from loan.api.loanpermissions import IsadminOrPostLoanPermission


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
    permission_classes = [IsadminOrPostLoanPermission]

    def get(self, request):        
        """
        Get all loan objects
        Only for the admin
        """                                
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
        :return: requester id, loan id and status
        """        
        # If user not exist, create it first and then the loan      
        requester_info = request.data.get('requester_info', None)
        requester = None
        if requester_info is not None: 
            try:               
                requester = Requester.objects.get(dni=request.data['requester_info']['dni'])
            except Requester.DoesNotExist:                
                # Create user
                requester_serializer = RequesterSerializer(data=requester_info)
                if requester_serializer.is_valid():
                    requester = requester_serializer.save()                    
                else:
                    return Response(requester_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Missing param": "requester_info"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data                
        data['requester'] = str(requester.id)
        loan_serializer = LoanCreatorSerializer(data=data)  
        dni = request.data['requester_info']['dni']                                                                                 
        request.data['state'] = loan_validator(dni)
        if loan_serializer.is_valid():                   
            new_loan = loan_serializer.save() 
            reponse_data = {
                "message": "Loan approved",
                "loan": loan_serializer.data
            }
            return Response(data=reponse_data, status=status.HTTP_201_CREATED)            
        else:
            return Response(loan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class LoanDetail(APIView):
    """    
    Get, update or delete a loan by id
    Methods only for the admin
    """    
    permission_classes = [IsadminOrPostLoanPermission]

    def get_object(self, id):
        try:
            return Loan.objects.get(id=id)
        except Loan.DoesNotExist:
            return None

    def get(self, request, pk):
        # Return a single instance of a loan
        loan = self.get_object(pk)
        loan_serializer =  LoanInfoSerializer(loan)
        return Response(loan_serializer.data)

    def delete(self, request, pk=None):        
        loan = self.get_object(pk)
        if loan is not None:
            loan.delete()
            return Response({"Message": "Loan request deleted"}, status=status.HTTP_204_NO_CONTENT)          
        return Response({"Message": "There is no loan request with id: " + str(pk)},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):        
        """
        Update loan state and amount
        request.data expected:
        {            
            "id": <Int>,
            "state": Enum('OK', 'NO'),
            "amount": <Float>,                
        }
        :return: modified loan state and amount
        """
        loan = self.get_object(pk)
        if loan is not None:
            loan_serializer = LoanModifySerializer(loan, data=request.data) 
            if loan_serializer.is_valid():
                loan_serializer.save()
                return Response(data=loan_serializer.data, status=status.HTTP_200_OK)
            return Response(loan_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        return Response({"Missing param": "pk"}, status=status.HTTP_400_BAD_REQUEST) 
