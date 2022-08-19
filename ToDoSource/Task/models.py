from django.db import models

# Create your models here.
class Tasks(models.Model):
    title = models.CharField(max_length=255)
    schedule = models.DateTimeField()
    milestone = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
