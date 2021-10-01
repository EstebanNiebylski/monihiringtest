from rest_framework import serializers
from users.models import Requester


class RequesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requester
        fields = ['email', 'dni', 'lastname', 'name', 'gender']

    def validate(self, data):        
        # Custom validator

        # admin name it's only for admin user        
        if data['name'] == 'admin' or data['lastname'] == 'admin':
            raise serializers.ValidationError({"admin": "is not a valid name."})                  
                
        # Validate only integers in dni
        if 'dni' in data:
            if not data['dni'].isdigit():
                raise serializers.ValidationError({"dni": "is not a valid. Positive integer only"})            
                
        return data    