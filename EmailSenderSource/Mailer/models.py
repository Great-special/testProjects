from django.db import models

# Create your models here.
class Message(models.Model):
    subject = models.CharField(max_length=125)
    body = models.TextField()
    
class EMails(models.Model):
    email = models.EmailField(max_length=150)