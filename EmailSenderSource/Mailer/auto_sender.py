import datetime
import schedule 
from hidden import mail_pass
from .alert import mailSender
from  . import models, forms

MESSAGES = []
UserAddress = []
# getting the week day from the date time 
# print(datetime.datetime.now().strftime('%H:%M'))
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


def clearer():
    MESSAGES.clear()
    UserAddress.clear()


# Automatically send Mails on scheduled
# Getting the messages and address added to list
def sendAutoMail():
    sender = 'tradevolatile@gmail.com'
    # mails = models.Message.objects.all()
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
                # checking for the models.Message and filtering by user
                mails = models.Message.objects.filter(user = username) 
                if mails:
                    for mail in mails:
                        # print(mail, mail.user) #django.contrib.auth.models.User
                        # print(type(mail.user), type(username))
                        # print(mail.user==username)
                        if mail.user == username: 
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
        # checking for the models.Email and filtering by group
        adrs = models.EMails.objects.filter(user=username, group=group)
        # adrs = models.EMails.objects.all().filter(user=msg['user'], group=group)
        if adrs:
            for adr in adrs:
                UserAddress.append(
                    {
                        "user": username,
                        "address": adr.email
                    }
                )
            
            
# Getting the messages and address from the list and sending the mail
def initialize_mailing():
    for msg in MESSAGES:
        # print(msg)
        print(msg['user'], msg['message'][3])
        user_name = msg['user']
        subject = f"Mail from {user_name} with subject {msg['message'][0]}"    
        body = msg['message'][1]
        day_repeated = msg['message'][2]
        group = msg['message'][3]

        if day_repeated == WeekDay:
            for adr in UserAddress:
                _uname = adr['user']
                receiver = adr['address']
                print(user_name, _uname)
                if user_name == _uname:
                    mailSender(
                    subject=subject, 
                    message=body, 
                    sender=sender, 
                    receiver=receiver, 
                    password=mail_pass
                    )
        elif day_repeated == "Everyday":
            for adr in UserAddress:
                _uname = adr['user']
                receiver = adr['address']
                print(user_name, _uname)
                if user_name == _uname:
                    mailSender(
                    subject=subject, 
                    message=body, 
                    sender=sender, 
                    receiver=receiver, 
                    password=mail_pass
                    )

# defining the schedule for sending emails
def sender():    
    schedule.every().day.at("12:00").do(clearer)
    schedule.every().day.at("07:00").do(sendAutoMail)
    schedule.every().day.at("09:00").do(initialize_mailing)
    while datetime.datetime.now().ctime() < "12.30":
        print('Yes')
        schedule.run_pending()
    
