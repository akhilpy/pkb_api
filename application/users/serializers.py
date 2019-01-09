from rest_framework import serializers
from django.contrib.auth import get_user_model
from random import  randint
class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30,required=True)
    mobile = serializers.IntegerField(required=True)

    def validate_mobile(self, value):
        """
        Validates mobile address
        :param value:
        :return: mobile as value if no exception raised
        """
        if not value:
            raise serializers.ValidationError('mobile is required field.')
        else:
            try:
                User = get_user_model()
                if not User.objects.filter(mobile=value).exists():
                    if len(str(value)) != 10:
                        raise serializers.ValidationError('mobile numer should be of 10 digits')
                    return value
                else:
                    raise serializers.ValidationError('mobile number is already registered.')
            except Exception as error:
                raise error

    def create(self, validated_data):
        """
        Register new user with validated_data
        :param validated_data:
        :return: Newly created user object
        """
        try:
            validated_data['otp'] =str(randint(1000, 9999))
            validated_data['username'] = validated_data['name'] + str(randint(1000000, 10000000))
            user = get_user_model().objects.create(**validated_data)
            print(user)
        except Exception as e:
            raise e
        return user


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)
