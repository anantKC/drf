from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

CustomUser = get_user_model()

class SignUpSerializer(ModelSerializer):
    password = serializers.CharField(required=True,min_length=8,write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)
    

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise exceptions.ValidationError("Email already exists")
        return value
        
    def validate(self,data):
            validated_data = super().validate(data)
            if validated_data['password'] != validated_data['confirm_password']:
                raise exceptions.ValidationError(
                {"password": ["Password fields didn't match."]}
            )
            return validated_data
        
    def create(self, validated_data):
        password = validated_data.pop("password")
        confirm_password = validated_data.pop("confirm_password")
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

    class Meta:
        model = CustomUser
        fields = ("email", "password", "confirm_password",)

class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ("email", "password",)

        @classmethod
        def get_token(cls,user):
            token = super().get_token(user)
            token["email"] = user.email
            return token
        
        def validate(self,data):
            user = authenticate(**data)
            if not user:
                raise exceptions.AuthenticationFailed
            user.save()
            refresh = self.get_token(user)
            response = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            return response

class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_new_password = serializers.CharField(required=True, min_length=8, write_only=True)

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except exceptions.ValidationError:
            raise serializers.ValidationError("Use strong password")
        return value

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password does not match.')
        return value

    def validate(self, data):
        validated_data = super().validate(data)
        if validated_data['new_password'] != validated_data['confirm_new_password']:
            raise serializers.ValidationError('Password fields did not match.')
        return validated_data

    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        instance.set_password(new_password)
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password', 'confirm_new_password']



                                
