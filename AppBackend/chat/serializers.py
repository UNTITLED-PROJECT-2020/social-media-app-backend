# imports
from .models import Account
# rest framework imports
from rest_framework import serializers

# creating serializers for models to work with


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        # fields = ['id', 'f_name', 'l_name',
        #           'email', 'ph_num', 'password', 'date']
        fields = ['email', 'username', 'password', 'ph_num']
        extra_kwargs = {
            'password': {'write_only': True}
        }
