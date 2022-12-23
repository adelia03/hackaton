from rest_framework import serializers

from review.serializers import FavoriteSerializer
from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')

    def validate(self, attrs):
        pass1 = attrs.get("password")
        pass2 = attrs.pop("password_confirm")
        if pass1 != pass2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        return email

    def create(self, validated_data):
        return User.objects.create_nonactive_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['favourite'] = FavoriteSerializer(instance.favourites.all(), many=True).data

        return rep

