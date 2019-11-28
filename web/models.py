from django.db import models
import datetime
# Create your models here.
class Family (models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Architecture (models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Vmachine(models.Model):
    name = models.CharField(max_length=50, null=True)
    littleEndian = models.BooleanField(null=True, default=True)
    instancePath = models.CharField(max_length=50)
    architecture = models.ForeignKey(Architecture, null=True, on_delete=models.SET_NULL)
    create_date = models.DateField(null=True)
    def __str__(self):
        return self.name




class Sample(models.Model):
    hash = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, null=True)
    instancePath = models.CharField(max_length=200)
    Vmachine_dst = models.ForeignKey(Vmachine,null=True,on_delete=models.SET_NULL)
    analisis = models.CharField(max_length=200)
    family = models.ForeignKey(Family, null=True, on_delete=models.SET_NULL)
    date = models.DateField(default=datetime.date.today)
    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return self.hash





