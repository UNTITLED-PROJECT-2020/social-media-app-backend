from django.db import models
from AppBackend import settings

# Create your models here.
#Accountdetail model
class Environments(models.Model):
    
    Name= models.CharField(max_length=20,unique=True)
    Description= models.CharField(max_length=300)
    created= models.DateTimeField(auto_now_add=True)
#    UserInEnvironments =models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)

class UserInEnv(models.Model):
    Env_Key=models.ForeignKey(Environments,on_delete=models.CASCADE)
    User_Key=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    class Meta:
        unique_together=[['Env_Key','User_Key']]
#User= settings.AUTH_USER_MODEL
#admin_user=User.objects.filter(username="admin")
#admin_user[0].environments_set.all()
#Req.user.environments_set.all()