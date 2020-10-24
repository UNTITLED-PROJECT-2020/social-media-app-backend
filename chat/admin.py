# imports
from django.contrib import admin
from .models import Message, Dialogue, ActiveDetail

# adding information to messages table


class MessageAdmin(admin.ModelAdmin):
    # shown in add
    fields = ('msg_from', 'msg_to', 'message',
              'command', 'sent_timestamp', 'dialogue')

    # shown in list view
    list_display = ('msg_from', 'msg_to', 'message',
                    'command', 'sent_timestamp', 'dialogue',)

    # filter list
    list_filter = ('msg_from', 'command',)

    # search parameters
    search_fields = ('msg_from', 'command', 'message',)


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


class ActiveDetailAdmin(admin.ModelAdmin):
    # shown in add
    fields = ('account', 'active', 'last_active',)

    # shown in list view
    list_display = ('account', 'active', 'last_active',)

    # filter list
    list_filter = ('account', 'active',)

    # search parameters
    search_fields = ('account', 'active',)


# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Dialogue, DialogueAdmin)
admin.site.register(ActiveDetail, ActiveDetailAdmin)
