from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import *
from django.contrib.auth import get_user_model
from user.permission import AccountUpdatePermission
Account = get_user_model()

class AccountViewset(viewsets.ModelViewSet):
    serializer_class = AccountSerializers
    queryset = Account.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AccountUpdatePermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'email',)

class TokenloginApiView(ObtainAuthToken): 
    serializer_class = AuthTokenSerializser
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
