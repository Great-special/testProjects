from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from multiselectfield import MultiSelectField

# from django.contrib.auth.models import AbstractUser


# Create your models here.

def get_user():
    users = User.objects.all()



class EMails(models.Model):
    Group_choice = (
        ('A', 'Group A'),
        ('B', 'Group B'),
        ('C', 'Group C'),
        ('D', 'Group D'),
    )

    email = models.EmailField(max_length=150)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=1)
    group = models.CharField(max_length=3, choices=Group_choice, default='A')
    def __str__(self):
        return self.email


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
    
    Group_choice = (
        ('A', 'Group A'),
        ('B', 'Group B'),
        ('C', 'Group C'),
        ('D', 'Group D'),
    )
    
    subject = models.CharField(max_length=125)
    body = models.TextField()
    receiver= models.CharField(max_length=3, choices=Group_choice, default='A')
    repeat = models.BooleanField(default=True)
    schedule = models.CharField(choices=ScheduleDays, max_length = 100, default='Monday')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    # Creating custom permissions
    # class Meta:
    #     permissions = [
    #         ("change_task_status", "Can change the status of tasks"),
    #         ("close_task", "Can remove a task by setting its status as closed"),
    #     ]
    
    def __str__(self):
        return self.subject
