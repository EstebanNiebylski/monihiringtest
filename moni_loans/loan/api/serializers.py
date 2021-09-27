from rest_framework import serializers
from loan.models import Loan
from user.api.serializers import UserSerializer

class LoanSerializer(serializers.ModelSerializer):
    requester = UserSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ['state', 'amount', 'requester']    
    