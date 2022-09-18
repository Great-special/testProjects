from django.db import models

# Create your models here.
class Message(models.Model):
    
    ScheduleDays = (
        ('Monday', 'Mondays'),
        ('Tuesday', 'Tuesdays'),
        ('Wednesday', 'Wednesdays'),
        ('Thursday', 'Thursdays'),
        ('Friday', 'Fridays'),
        ('Saturday','Saturdays'),
        ('Sunday', 'Sundays'),
        ('Everyday', 'Everyday')
    )
    
    subject = models.CharField(max_length=125)
    body = models.TextField()
    repeat = models.BooleanField(default=True)
    schedule = models.CharField(choices=ScheduleDays, max_length = 100)
    
    def __str__(self):
        return self.subject
    
    
class EMails(models.Model):
    email = models.EmailField(max_length=150)
    
    def __str__(self):
        return self.email