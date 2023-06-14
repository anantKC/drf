from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from users.serializers import (
    SignUpSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
)

class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
                "message": "User successfully created",
                "data": [serializer.validated_data],
            },status=status.HTTP_201_CREATED)

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({
            "message": "User successfully logged in",
            "data": [serializer.validated_data],
            },status=status.HTTP_200_OK)
    
class PasswordChangeView(APIView):
    serializer_class = PasswordChangeSerializer
    # permission_classes = [IsAuthenticated]

    def post(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,instance=request.user,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
                "message": "Password successfully changed",
                "data": [serializer.validated_data],
            },status=status.HTTP_200_OK)
