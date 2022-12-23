from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail

from .serializers import RegisterUserSerializer, UserSerializer, CreateNewPasswordSerializer
from .models import User



class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Вы успешно зарегистрировались', status=201)


@api_view(['DELETE'])
def delete(request, email):
    user = get_object_or_404(User, email=email)
    if user.is_staff:
        return Response(status=403) # запрещаем
    user.delete()
    return Response('Успешно удалили акаунт', status=204)


@api_view(['GET'])
def activate_view(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True # activate user
    user.activation_code = '' # delete the activated code
    user.save()
    return Response('Successfuly activated the account', 200)

@api_view(['GET'])
def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    return Response(UserSerializer(user).data, status=200)

    return Response(UserSerializer(user).data, status=200)


def send_activation_code(email, activation_code):
    activation_url = f'localhost:8000/account/forgot-password-complete/{activation_code}'
    message = f"""Чтобы восстановить пароль, пройдите по данной ссылке: {activation_url}"""
    send_mail('Восстановление пароля', message, 'admin@admin.com',recipient_list=[email],)

class ForgotPassword(APIView):

    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code(user.email, user.activation_code)
        return Response('Вам отправлено письмо', status=200)


class ForgotPasswordComplete(APIView):

    def post(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.activation_code = ''
        serializer = CreateNewPasswordSerializer(data=request.data)
        user.is_active = True
        user.save()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно восстановили пароль', status=200)
