from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from posts.serializers import PostsSerializer
from posts.models import Posts
from posts.permissions import CustomAdminPermissions
# Create your views here.

class PostView(ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticated, CustomAdminPermissions]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message":"Post created successfully",
            "data": serializer.data
        },status=status.HTTP_201_CREATED)

    

