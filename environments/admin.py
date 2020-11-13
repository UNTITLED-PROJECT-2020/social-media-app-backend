from django.contrib import admin
from .models import Environments,UserInEnv
# Register your models here.
admin.site.register(Environments)
admin.site.register(UserInEnv)