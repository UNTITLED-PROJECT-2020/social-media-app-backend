from rest_framework import serializers
from .models import AccountDetail
from authentication.serializers import AccountSerializer


class AccountDetailSerializer(serializers.ModelSerializer):
    account= AccountSerializer(read_only=True)

    class meta:
        model = AccountDetail
        fields=['fname','lname','bio','score','created','account']
