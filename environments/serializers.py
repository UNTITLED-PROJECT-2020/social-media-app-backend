from rest_framework import serializers
from .models import Environments, UserInEnv

class EnvironmentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Environments
        fields = [
            'id','Name','Description','created'
        ]
class UserInEnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInEnv
        fields=[
            'id','Env_Key','User_Key'
        ]