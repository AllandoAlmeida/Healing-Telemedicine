from django.db import models
from doctor.models import OpenDate
from django.contrib.auth.models import User

# Create your models here.

class Query(models.Model):
    status_choices = (
        ('A', 'Agendada'),
        ('F', 'Finalizada'),
        ('C', 'Cancelada'),
        ('I', 'Iniciada')

    )
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    open_date = models.ForeignKey(OpenDate, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=status_choices, default='A')
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.patient.username
    
    
class Document(models.Model):
    query = models.ForeignKey(Query, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=30)
    document = models.FileField(upload_to='documents')

    def __str__(self):
        return self.title
  