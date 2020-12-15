# imports
from django.contrib import admin
from .models import Message, Dialogue, ActiveDetail, GroupMessage, Group, RoomMessage, Room

# adding information to messages table


class DialogueAdmin(admin.ModelAdmin):
    # shown in add
    fields = ('sender', 'receiver', 'last_received_receiver',
              'last_seen_receiver',)

    # shown in list view
    list_display = ('sender', 'receiver',
                    'last_received_receiver', 'last_seen_receiver',)

    # filter list
    list_filter = ('sender', 'receiver',)

    # search parameters
    search_fields = ('sender', 'receiver',)

class MessageAdmin(admin.ModelAdmin):
    # shown in add
    fields = ('msg_from', 'msg_to', 'message',
              'command', 'sent_timestamp', 'dialogue')

    # shown in list view
    list_display = ('msg_from', 'msg_to', 'message',
                    'command', 'sent_timestamp', 'dialogue',)

    # filter list
    list_filter = ('msg_from', 'msg_to', 'command',)

    # search parameters
    search_fields = ('msg_from', 'command', 'message',)


class ActiveDetailAdmin(admin.ModelAdmin):
    # shown in add
    fields = ('account', 'active', 'last_active',)

    # shown in list view
    list_display = ('account', 'active', 'last_active',)

    # filter list
    list_filter = ('account', 'active',)

    # search parameters
    search_fields = ('account', 'active',)


class GroupAdmin(admin.ModelAdmin):
    # shown in add
    fields = ('name', 'key', 'bio', 'participants', 'admin',)

    # shown in list view
    list_display = ('name', 'key', 'bio',)

    # filter list
    list_filter = ('name', 'bio',)

    # search parameters
    search_fields = ('name', 'bio',)


class GroupMessageAdmin(admin.ModelAdmin):
    # shown in add
    fields = ('msg_from', 'msg_to', 'message',
              'command', 'sent_timestamp', 'pending', 'group',)

    # shown in list view
    list_display = ('msg_from', 'msg_to', 'message',
                    'command', 'sent_timestamp', 'group',)

    # filter list
    list_filter = ('msg_from', 'msg_to', 'command', 'group',)

    # search parameters
    search_fields = ('msg_from', 'command', 'message', 'group',)


class RoomAdmin(admin.ModelAdmin):
    # shown in add
    fields = ('participants', 'active', 'created', 'finished')

    # shown in list view
    list_display = ('__str__', 'active', 'created', 'finished')

    # filter list
    list_filter = ('active', 'created',)

    # search parameters
    search_fields = ('active', 'created',)

    # fields that are automatically created
    readonly_fields = ('created', 'finished')


class RoomMessageAdmin(admin.ModelAdmin):
    # shown in add
    fields = ('msg_from', 'msg_to', 'message',
              'command', 'sent_timestamp', 'room')

    # shown in list view
    list_display = ('msg_from', 'msg_to', 'message',
                    'command', 'sent_timestamp', 'room',)

    # filter list
    list_filter = ('msg_from', 'msg_to', 'command', 'room',)

    # search parameters
    search_fields = ('msg_from', 'command', 'message', 'room',)





# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Dialogue, DialogueAdmin)
admin.site.register(ActiveDetail, ActiveDetailAdmin)
admin.site.register(GroupMessage, GroupMessageAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(RoomMessage, RoomMessageAdmin)
admin.site.register(Room, RoomAdmin)
