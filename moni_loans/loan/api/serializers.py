from rest_framework import serializers
from loan.models import Loan
from users.api.serializers import RequesterSerializer
from users.models import Requester


class LoanInfoSerializer(serializers.ModelSerializer):    
    # Serializer for return the user info
    requester = RequesterSerializer()

    class Meta:
        model = Loan
        fields = ['state', 'amount', 'requester']  

class LoanCreatorSerializer(serializers.ModelSerializer):    
    # Serializer for create a new loan        

    class Meta:
        model = Loan
        fields = ['amount', 'requester', 'state']  

    def validate(self, data):
        # Custom validator

        # Validate amount > 0         
        if 'amount' in data:
            if data['amount'] < 0:
                serializers.ValidationError('"amount" need to be a positive float.')
        else:
            raise serializers.ValidationError('"amount" is missing.')

        return data