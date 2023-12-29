from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import serializers
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject
from rest_framework.fields import SkipField
from django.conf import settings
from buyer_app.models import Buyer
from seller_app.models import Seller
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from helper_files.serializer_helper import SerializerHelper
from helper_files.status_code import Status_code
from helper_files.cryptography import AESCipher
from typing import Dict, Any

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class RegisterationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'is_staff', 'first_name', 'last_name',
                  'is_superuser', 'id',]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'is_staff': {'default': False},
            'is_superuser': {'default': False},
        }

    def save(self, validated_data):
        account = User(email=validated_data['email'], username=validated_data['username'],
                       is_staff=validated_data['is_staff'], first_name=validated_data['first_name'],
                       last_name=validated_data['last_name'],
                       is_superuser=validated_data['is_superuser'],
                       )
        account.set_password(validated_data['password'])
        account.save()

        return account

    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self, raise_exception=raise_exception)

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )


class UserSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )

    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'first_name', 'last_name',
                  'is_superuser', 'id']


#
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        user = UserProfile.objects.filter(user=self.user)

        if user:
            user_id = user[0].id

            buyer_id = Buyer.objects.filter(user_id=user_id)
            seller_id = Seller.objects.filter(user_id=user_id)

            if buyer_id and seller_id:
                data['buyer_id'] = aes.encrypt(str(buyer_id[0].id))
                data['seller_id'] = aes.encrypt(str(seller_id[0].id))
                data['message'] = 'User is both a Buyer and a Seller.'
                data['status_code'] = Status_code.success

            elif buyer_id:
                data['buyer_id'] = aes.encrypt(str(buyer_id[0].id))
                data['message'] = 'User is a Buyer'
                data['status_code'] = Status_code.success

            elif seller_id:
                data['seller_id'] = aes.encrypt(str(seller_id[0].id))
                data['message'] = 'User is a Seller'
                data['status_code'] = Status_code.success

            else:
                data['message'] = 'User need to be registered as a Buyer or a Seller.'
                data['status_code'] = Status_code.unauthorized

        return data
