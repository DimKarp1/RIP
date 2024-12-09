from django.db import models
from django.contrib.auth import get_user_model

class Component(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    shortDescription = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    imgSrc = models.CharField(max_length=100, null=True)
    
class Assembly(models.Model):
    id = models.AutoField(primary_key=True)
    dateCreated = models.DateField(auto_now_add=True)
    status = models.CharField(default="draft")
    creator = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='userAccess')
    moder = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='moderAccess', null=True)
    dateModerated = models.DateField(null=True)
    dateSaved = models.DateField(null=True)
    satelliteName = models.CharField(max_length=150, null=True)
    flyDate = models.DateField(null=True)
    orbit = models.IntegerField(null=True)
    
    
class MM(models.Model):
    id = models.AutoField(primary_key=True)
    idComp = models.ForeignKey(Component, on_delete=models.DO_NOTHING)
    idAssembly = models.ForeignKey(Assembly, on_delete=models.DO_NOTHING)
    count = models.IntegerField(null=True)
    
    class Meta:
        unique_together = (('idComp', 'idAssembly'),)
