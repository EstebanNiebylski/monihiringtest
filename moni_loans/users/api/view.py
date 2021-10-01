from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Requester
from users.api.serializers import RequesterSerializer


class RequesterApiView(APIView):    
    """
    Get or create a requester
    """
    def get(self, request):    
        requester = Requester.objects.all()
        requester_serializer = RequesterSerializer(users, many=True)                     
        return Response(requester_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        requester_serializer = RequesterSerializer(data=request.data) 
        if requester_serializer.is_valid():
            requester_serializer.save()
            return Response(requester_serializer.data)
        return Response(requester_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
