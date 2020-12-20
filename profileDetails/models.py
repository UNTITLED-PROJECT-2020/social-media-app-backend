from django.db import models
from AppBackend import settings
from environments.models import Environments

# Create your models here.
#Accountdetail model
class AccountDetail(models.Model):
    fname= models.CharField(max_length=100)
    lname= models.CharField(max_length=100)
    bio= models.TextField(max_length=200)
    score=models.IntegerField()
    #batch=models.IntegerField()
    #issues with existing columns
    created= models.DateTimeField(auto_now_add=True)
    account=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True)
    #img


class Ledger(models.Model):
    env=models.ForeignKey(Environments,on_delete=models.CASCADE)
    account=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True)
    score=models.IntegerField()
    ph_num=models.CharField(max_length=10)
    created= models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=[["env","account"]]
        ordering = ("account","score","created")