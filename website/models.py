from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Credential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    credential_name= models.CharField(max_length=128) 
    credential_url= models.URLField(max_length=200, null=True, blank=True)
    credential_login = models.CharField(max_length=128)
    credential_password = models.CharField(max_length=512)
    def __str__(self):
        return self.user.username+': '+self.credential_name
    class Meta:
        ordering = ['id']