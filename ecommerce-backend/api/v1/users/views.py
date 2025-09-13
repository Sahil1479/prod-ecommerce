from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from core.models import User
from .serializers import UserSerializer

class RegisterAPIView(APIView):
    """
    Register a new user.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListAPIView(APIView):
    """
    List all users.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

class UserDetailAPIView(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if(request.user.id != pk and not request.user.is_staff):
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
