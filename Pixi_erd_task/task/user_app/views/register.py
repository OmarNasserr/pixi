from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ..validation import UserAppValidation
from ..serializers import RegisterationSerializer
from ..models import UserProfile
from buyer_app.models import Buyer
from seller_app.models import Seller
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code

aes = AESCipher(settings.SECRET_KEY[:16], 32)


@api_view(['Post',])
def registeration_view(request):

    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)

        data = {}
        valid, err = serializer.is_valid(raise_exception=False)
        response = UserAppValidation.validate_user_create(
            request.data, valid, err)

        if response.status_code == 400:
            return response

        # we override the save method and it returns an account now
        account = serializer.save(serializer.validated_data)
        print(request.data['is_buyer'])
        print(request.data['is_seller'])

        buyer_id = False
        seller_id = False

        if request.data['is_buyer']:
            if str(request.data['is_buyer']).lower() == 'true':
                user_profile = UserProfile.objects.create(user=account,is_buyer=True)
                buyer_id = Buyer.objects.create(user_id=user_profile,)
                user_profile.is_buyer = True

        if request.data['is_seller']:
            if str(request.data['is_seller']).lower() == 'true':
                if buyer_id:
                    user_profile.is_seller = True
                    seller_id = Seller.objects.create(user_id=user_profile,)
                else:
                    user_profile = UserProfile.objects.create(user=account, is_seller=True)
                    seller_id = Seller.objects.create(user_id=user_profile,)
                    user_profile.is_seller = True




        data['response'] = "Registeration Successful"
        data['id'] = aes.encrypt(str(account.id))
        data['username'] = account.username
        data['email'] = account.email

        if buyer_id:
            data['buyer_id'] = aes.encrypt(str(buyer_id.id))
        if seller_id:
            data['seller_id'] = aes.encrypt(str(seller_id.id))

        # JWT token
        refresh = RefreshToken.for_user(account)
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(data, status=Status_code.created)
