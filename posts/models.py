from django.db import models

from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Posts(models.Model):
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

