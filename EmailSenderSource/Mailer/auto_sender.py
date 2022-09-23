import datetime

from hidden import mail_pass
from .alert import mailSender
from  . import models, forms

MESSAGES = []

# getting the week day from the date time 
weekday = datetime.datetime.now().weekday()

if weekday == 0:
    WeekDay = 'Monday'
elif weekday == 1:
    WeekDay = 'Tuesday'
elif weekday == 2:
    WeekDay = 'Wednesday'
elif weekday == 3:
    WeekDay = 'Thursday'
elif weekday == 4:
    WeekDay = 'Friday'
elif weekday == 5:
    WeekDay = 'Saturday'
elif weekday == 6:
    WeekDay = 'Sunday'


# Automatically send Mails on scheduled
def sendAutoMail():
    sender = 'tradevolatile@gmail.com'
    mails = models.Message.objects.all()
    # adr = models.EMails.objects.all()
    user = models.User.objects.all()
    # print(user)
    # print(type(user))
    # checking for the django models.User
    if user:
        for u in user:
            # print(type(u)) #django.contrib.auth.models.User
            if not u.is_superuser:
                username = u
                # print(f" {username} is not superuser")
                # checking for the models.Messages
                if mails:
                    for mail in mails:
                        # print(mail, mail.user) #django.contrib.auth.models.User
                        # print(type(mail.user), type(username))
                        # print(mail.user==username)
                        if mail.user == username: 
                            # print('yes')
                            subject = mail.subject
                            message = mail.body
                            repeat_day = mail.schedule
                            group = mail.receiver
                            
                            MESSAGES.append(
                                {
                                 "user": username,
                                 "message":[subject, subject, repeat_day, group]
                                }
                            )
                            
    for msg in MESSAGES:
        # print(msg)
        # print(msg['user'], msg['message'][3])
        subject = f"Mail from {msg['user']} with subject {msg['message'][0]}"    
        body = msg['message'][1]
        day_repeated = msg['message'][2]
        group = msg['message'][3]
        
        
        if WeekDay != day_repeated:
            print('yess')
            
            # checking for the models.Email
            adrs = models.EMails.objects.filter(group=group)
            if adrs:
                print(adrs)
                for adr in adrs:
                    receiver = adr
                    print(receiver)
                
                mailSender(
                subject=subject, 
                message=body, 
                sender=sender, 
                receiver=receiver, 
                password=mail_pass
                )
          
                   
sendAutoMail()