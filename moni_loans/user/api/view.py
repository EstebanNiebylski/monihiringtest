from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from user.models import User
from user.api.serializers import UserSerializer

@api_view(['GET', 'POST'])
def user_list(request):    

    if request.method == 'GET':               
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)                     
        return Response(user_serializer.data)
    elif request.method == 'POST':
        user_serializer = UserSerializer(data= request.data) 
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
def get_user_from_dni(request, dni=None):
    
    if dni is not None:
        try:
            user = User.objects.get(dni=dni)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            user_serializer = UserSerializer(user) 
            return Response(user_serializer.data)

