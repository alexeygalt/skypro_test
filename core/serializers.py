from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

USER_MODEL = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ("username", "first_name", "last_name", "email", "password")
        extra_kwargs = {'password': {"write_only": True}}

    def create(self, validated_data):
        instance = USER_MODEL.objects.create_user(**validated_data)
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)

    class Meta:
        model = USER_MODEL
        fields = ("username", "password")
        extra_kwargs = {'password': {"write_only": True}}

    def save(self, **kwargs):
        instance = authenticate(username=self.validated_data.get('username'),
                                password=self.validated_data.get('password'))
        if not instance:
            raise ValidationError({"Ошибка входа": "Неправильный логин или пароль"})

        login(self.context["request"], instance)
        return instance
