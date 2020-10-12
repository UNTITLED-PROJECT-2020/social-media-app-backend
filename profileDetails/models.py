from django.db import models
from AppBackend import settings

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
    Account_foreignkey=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    #img