from django.db import models
from AppBackend import settings

# Create your models here.
#class Account(models.Model):
#    email= models.EmailField(max_length=100)
#    phone= models.PositiveBigIntegerField()
#    password=models.CharField(max_length=100)
#    lastactive= models.DateTimeField(auto_now=True)
    #env
    
class AccountDetail(models.Model):
    fname= models.CharField(max_length=100)
    lname= models.CharField(max_length=100)
    bio= models.TextField(max_length=200)
    score=models.CharField(max_length=1)
    created= models.DateTimeField(auto_now_add=True)
    account=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    #img

#def __str__(self):
#    return self.username