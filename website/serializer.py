from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Credential


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]

class CredentialSerializer(serializers.ModelSeHyperlinkedModelSerializerrializer):

    class Meta:
        model = Credential
        fields = []