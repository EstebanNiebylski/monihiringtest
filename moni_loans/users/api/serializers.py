from rest_framework import serializers
from users.models import Requester


class RequesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requester
        fields = ['email', 'dni', 'lastname', 'name', 'gender']

    def validate(self, data):        
        print("::::DATAREQUESTER:::_")
        print(data)
        # Custom validator

        # admin name is for admin user        
        if data['name'] == 'admin' or data['lastname'] == 'admin':
            raise serializers.ValidationError({"admin": "is not a valid name."})        
        # Validate email        
                
        return data    