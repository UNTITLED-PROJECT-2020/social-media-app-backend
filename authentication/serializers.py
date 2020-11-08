# imports
from .models import Account
# rest framework imports
from rest_framework import serializers

# creating serializers for models to work with


class AccountSerializer(serializers.ModelSerializer):

    # setting password to "write-only" i.e. not returning as response
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        # fields = ['id', 'f_name', 'l_name',
        #           'email', 'ph_num', 'password', 'date']
        fields = ['email', 'username', 'password', 'ph_num']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # overriding save method to be accessed by signup class
    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            ph_num=self.validated_data['ph_num'],
        )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account
