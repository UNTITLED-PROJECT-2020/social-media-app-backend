# imports
from django.contrib import admin
from .models import Message

# adding information to messages table


class MessageAdmin(admin.ModelAdmin):
    # shown in add
    fields = ('sender', 'receiver', 'message',
              'command', 'sent_timestamp',)

    # shown in list view
    list_display = ('sender', 'receiver', 'message',
                    'command', 'sent_timestamp',)

    # filter list
    list_filter = ('sender', 'command',)

    # search parameters
    search_fields = ('semder', 'command', 'message',)


# Register your models here.
admin.site.register(Message, MessageAdmin)
