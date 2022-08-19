from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)


class Team(models.Model):
    name = models.CharField(max_length=200)
    team_lead = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    
    def __str__(self):
        return self.name
        
class TeamMember(Team):
    team_members = models.ManyToManyField(User)
    
# def post_user_created_signal(sender, instance, created, **kwargs):
#     print(instance)
#     print(created)
#     if created:
#         Team.objects.create(name="Team A", user=instance)

# post_save.connect(post_user_created_signal, sender=User)