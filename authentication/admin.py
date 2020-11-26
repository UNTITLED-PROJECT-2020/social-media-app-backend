from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.


class AccountAdmin(UserAdmin):  # registering manager
    list_display = ('pk', 'email', 'username', 'ph_num', 'date_joined',
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('pk', 'email', 'username',)
    readonly_fields = ('pk', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# registering all models
admin.site.register(Account, AccountAdmin)
