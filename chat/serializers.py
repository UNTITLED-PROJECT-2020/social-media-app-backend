# imports
import uuid

from django.http.response import JsonResponse
from .models import Message, Dialogue, GroupMessage, Group
from django.contrib.auth import get_user_model as User
# rest framework imports
from rest_framework import exceptions
from rest_framework import serializers

# creating serializers for models to work with


# serializing Dialogues
class DialogueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dialogue
        fields = ['sender', 'receiver', 'last_received_receiver',
                  'last_seen_receiver', ]


# serializing Messages
class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'msg_from', 'msg_to', 'message',
                  'command', 'sent_timestamp', 'dialogue']


# serializing Groups
class GroupSerializer(serializers.ModelSerializer):
    # adding slug fiels to get phone numbers of people in many-to-many field
    participants = serializers.SlugRelatedField(
        many=True,
        slug_field="ph_num",
        queryset=User().objects.all())
    admin = serializers.SlugRelatedField(
        many=True,
        slug_field="ph_num",
        queryset=User().objects.all())

    class Meta:
        model = Group
        fields = ['name', 'key', 'bio', 'participants', 'admin']

    def create(self, validated_data):
        # error handling
        try:
            print(validated_data)
            # adding empty m2m field
            participants = validated_data.pop('participants')
            admin = validated_data.pop('admin')

            # generating key
            while True:
                grp_key = uuid.uuid4().hex[:10].upper()

                try:
                    group = Group.objects.get(key=grp_key)

                except Group.DoesNotExist:
                    validated_data['key'] = grp_key
                    break

            # Create Group Message Instance
            instance = self.Meta.model.objects.create(**validated_data)

            # adding m2m relation
            for user in admin:
                print(user)
                instance.admin.add(user)

                if user not in participants:
                    participants.append(user)

            for user in participants:
                instance.participants.add(user)

        except exceptions.ValidationError as e:
            errors_messages = e.error_dict if hasattr(
                e, 'error_dict') else e.error_list

            # raise serializers.ValidationError(errors_messages)
            return JsonResponse(serializers.ValidationError(errors_messages))

        # returning json instance of the created message
        return GroupSerializer(instance).data


# serializing Groups Messages
class GroupMessageSerializer(serializers.ModelSerializer):
    # adding slug fiels to get phone numbers of people in many-to-many field
    pending = serializers.SlugRelatedField(
        many=True,
        slug_field="ph_num",
        queryset=User().objects.all())

    class Meta:
        model = GroupMessage
        fields = ['msg_from', 'msg_to', 'message',
                  'command', 'sent_timestamp', 'pending', 'group']

    def create(self, validated_data):
        # error handling
        try:
            # adding empty m2m field
            validated_data.pop('pending')

            # getting the key of the group
            group_key = validated_data['msg_to']

            # creating related group and adding primary key to validated data
            group = Group.objects.get(key=group_key)
            validated_data['group'] = group

            # specifying the command to be accessed on ChatSpecialConsumer
            validated_data['command'] = "new_msg"

            # Create Group Message Instance
            instance = self.Meta.model.objects.create(**validated_data)

            # creating people set
            people = group.participants.all()

            # adding m2m relation
            for person in people:
                if person.ph_num != validated_data['msg_from']:
                    instance.pending.add(person)

        except exceptions.ValidationError as e:
            errors_messages = e.error_dict if hasattr(
                e, 'error_dict') else e.error_list
            raise serializers.ValidationError(errors_messages)

        # returning json instance of the created message
        return GroupMessageSerializer(instance).data
