from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserCreateSerializer, TokenSerializer
from random import randint
from rest_framework import status as http_status_codes
from django.utils import timezone
from django.contrib.auth import authenticate, get_user_model
from .models import AuthUserLog
from rest_framework_jwt.settings import api_settings
from .models import CustomUser as User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginApiView(APIView):
    queryset = User.objects.all()
    def post(self, request):
        mobile = request.data.get('mobile', None)
        otp = request.data.get('otp', None)
        if mobile and otp:
            try:
                user = authenticate(mobile=mobile, otp=otp)
                if user:
                    user.last_login = timezone.now()
                    user.save()

                    auth_user_log = AuthUserLog()
                    auth_user_log.ip_address = request.META['REMOTE_ADDR']
                    auth_user_log.user_agent = request.META['HTTP_USER_AGENT']
                    auth_user_log.user = user
                    auth_user_log.save()

                    serializer = TokenSerializer(data={
                        # using drf jwt utility functions to generate a token
                        "token": jwt_encode_handler(jwt_payload_handler(user)),
                    })

                    if serializer.is_valid():
                        return Response(serializer.data)
                    return Response({'message': 'You have been successfully logged in', 'data': serializer },
                                    status=http_status_codes.HTTP_200_OK)
                else:
                    return Response({'message':'Invalid credentials.', 'data': {}},status=http_status_codes.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                print('##########')
                print(e)
                print('############')
                return Response({'message': 'Server error.', 'data': {}},status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'email and otp are required fields', 'data': {}}, status=http_status_codes.HTTP_400_BAD_REQUEST)



# Create your views here.
class UserCreateApiView(APIView):
    # @jwt_check(module_action_list=[user_create])
   # @jwt_check()
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user=serializer.save()
                return Response({'message': "user_created", 'data': {'otp':user.otp}},
                                status=http_status_codes.HTTP_201_CREATED)
            except Exception as e:
                return Response({'message': 'Server error.', 'data': {}}, status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message': 'error','error': tmp_errors, 'data': {}}, status=http_status_codes.HTTP_400_BAD_REQUEST)

