from rest_framework import serializers
from .models import Environments

class EnvironmentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Environments
        fields = [
            'id','Name','Description','created','UserInEnvironments'
        ]