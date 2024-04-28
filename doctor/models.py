from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


def is_doctor(user):
  return MedicalData.objects.filter(user=user, specialty__isnull=False).exists()

# Create your models here.
class Specialties(models.Model):    
    specialty = models.CharField(max_length=100)
    

    def __str__(self):
         return self.specialty


class MedicalData(models.Model):
     crm = models.CharField(max_length=30)
     name = models.CharField(max_length=100)
     zidCode = models.CharField(max_length=15)
     street = models.CharField(max_length=100)
     neighborhood = models.CharField(max_length=100)
     number = models.IntegerField()
     register_geral = models.ImageField(upload_to="rgs")
     medical_identity_card = models.ImageField(upload_to='mic')
     photo = models.ImageField(upload_to="fotos_profil")
     description = models.TextField(null=True, blank=True)
     query_value = models.FloatField(default=100)
     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
     specialty = models.ForeignKey(Specialties, on_delete=models.DO_NOTHING, null=True, blank=True)

     def __str__(self):
         return self.user.username
     
     @property
     def next_date(self):
         next_date = OpenDate.objects.filter(user=self.user).filter(date__gt=datetime.now()).filter(scheduled=False).order_by('date').first()
         return next_date
     
     
     
class OpenDate(models.Model):
     date = models.DateTimeField()
     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
     scheduled = models.BooleanField(default=False)

     def __str__(self):
         return str(self.date)  
