from django.urls import path,include
from rest_framework.routers import DefaultRouter
from posts.views import PostView
routers = DefaultRouter()
routers.register(r'', PostView)

urlpatterns = [
    path('', include(routers.urls)),
]