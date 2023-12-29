from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User

from ..serializers import UserSerializer
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code

aes = AESCipher(settings.SECRET_KEY[:16], 32)


    
class UserDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):

    serializer_class=UserSerializer
    queryset=User.objects.all()

    def get_object(self):
        try:
            pk = aes.decrypt(str(self.kwargs['user_id']))
            user=User.objects.filter(pk=int(pk))
            obj = user[0]
            print(obj)
        except:
            return ValueError('wrong id format')
        if user.count() == 0:
            return ValueError('wrong id format')
        
        self.check_object_permissions(self.request, obj)
        return obj
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        if str(type(instance)) != "<class 'django.contrib.auth.models.User'>":
            return Response(data={"message": "User wasn't found.",
                              "status":Status_code.no_content},status=Status_code.no_content)
        return super().update(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'django.contrib.auth.models.User'>":
            return Response(data={"message": "User wasn't found.",
                              "status":Status_code.no_content},status=Status_code.no_content)
        return self.retrieve(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'django.contrib.auth.models.User'>":
            return Response(data={"message": "User wasn't found.",
                              "status":Status_code.no_content},status=Status_code.no_content)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "User was deleted successfully.",
                              "status":Status_code.no_content},status=Status_code.no_content)
