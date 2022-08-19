from django.db import models
from users.models import User, Team


# Create your models here.

class Lead(models.Model):
    title = models.CharField(max_length = 100)
    account_name = models.CharField(max_length = 150)
    contact_name = models.CharField(max_length = 150, null=False)
    email = models.EmailField(max_length = 200)
    phone = models.CharField(max_length = 11)
    manager = models.ForeignKey(Team, null=True, blank=True, on_delete = models.SET_NULL)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.title
    
    
class Task(models.Model):
    PRIORITY_CHOICES = (
        ('H', 'HIGH'),
        ('M', 'MEDIUM'),
        ('L', 'LOW'),
    )
    
    TASK_TYPE = (
        ('PHONE', 'PHONE CALL'),
        ('EMAIL', 'EMAIL'),
        ('VISIT', 'VISITATION'),
        ('MEETINGS', 'MEETINGS'),
        ('PROPOSAL', 'SEND PROPOSAL'),
    )
    
    date = models.DateTimeField()
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length = 100)
    task_type = models.CharField(choices=TASK_TYPE, max_length = 100)
    description = models.TextField()
    owner = models.OneToOneField(User, on_delete = models.CASCADE)
    status = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)
    action_on = models.ForeignKey(Lead, on_delete = models.CASCADE) 
    
    
    def __str__(self): 
        return self.task_type + '       ' + self.priority  
    

class Activitie(models.Model):

    ACTIVITY_TYPE = (
        ('PHONE', 'PHONE CALL'),
        ('EMAIL', 'EMAIL'),
        ('VISIT', 'VISITATION'),
        ('MEETINGS', 'MEETINGS'),
        ('PROPOSAL', 'SEND PROPOSAL'),
    )
    
    date = models.DateTimeField()
    activity_type = models.CharField(choices=ACTIVITY_TYPE, max_length = 100)
    description = models.TextField()
    # attachment = models.FileField(upload_to='')
    executor = models.ForeignKey(User, on_delete = models.CASCADE) 
    status = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)
    action_on = models.ForeignKey(Lead, on_delete = models.CASCADE) 
    
    
    def __str__(self): 
        return self.activity_type