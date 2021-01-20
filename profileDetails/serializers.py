from rest_framework import serializers
from .models import AccountDetail, Ledger

class AccountDetailSerializer(serializers.ModelSerializer):
    # account key commented out for now
    class Meta:
        model = AccountDetail
        fields = [ 'fname', 'lname', 'bio',
                  'score', 'created', 'account']
class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ledger
        fields=['env','account','score','created','ph_num']