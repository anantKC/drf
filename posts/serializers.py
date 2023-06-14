from rest_framework import serializers

from posts.models import Posts


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id','title', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

        def validate(self,value):
            validated_data = super().validate(value)
            return validated_data
