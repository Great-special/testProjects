from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from  . import models, forms
from django.contrib.auth.decorators import login_required

from hidden import mail_pass
from .alert import mailSender
import schedule 

# Create your views here.

MailingList = []
# Note that the method must be in Upper Case POST GET PUT
def index(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        sender = request.POST.get("sender-email")
        receiver = request.POST.get("email")
        
        print(message, sender, receiver, subject)
        if not sender:
            sender = 'tradevolatile@gmail.com'
        
        mailSender(
            subject=subject, 
            message=message, 
            sender=sender, 
            receiver=receiver, 
            password=mail_pass
        )
        messages.add_message(request, messages.INFO, "your message was sent")
        # send_mail(
        #     subject,
        #     message,
        #     sender,
        #     [receiver],
        #     fail_silently=False,
        # )
        
        return redirect('express-mail')
    return render(request, template_name='index.html')

@login_required(login_url="login")
def getEmails(request):
    form = forms.EmailsForm()
    
    if request.user.is_authenticated:
        user = request.user
    if request.method == 'POST':
        email = request.POST.get('email')
        MailingList.append(email)
        
        for mail in MailingList:
            models.EMails.objects.create(email=mail, user=user)
            messages.add_message(request, messages.INFO, "your email address has been added")
        
        context = {'form': form}
        return render(request, template_name='add_email.html', context=context)
    else:
        context = {'form': form}
        return render(request, template_name='add_email.html', context=context)


@login_required(login_url="login")
def listMail(request):
    if request.user.is_authenticated:
        messages = models.Message.objects.filter(user=request.user)
    
    context = {
        'messages': messages
    }
    
    return render(request, template_name='list_mail.html', context=context)

@login_required(login_url="login")
def createMail(request):
    
    if request.user.is_authenticated:
        user = request.user
        
    message_form = forms.MessageForm()
    
    if request.method == 'POST':
        message_form = forms.MessageForm(request.POST)
        if message_form.is_valid():
           
           
            subject = message_form.cleaned_data['subject']
            body = message_form.cleaned_data['body']
            repeat = message_form.cleaned_data['repeat']
            schedule = message_form.cleaned_data['schedule']
            
            models.Message.objects.create(
                subject=subject,
                body=body,
                repeat=repeat,
                schedule=schedule,
                user=user
            )
            messages.add_message(request, messages.INFO, f"You have successfully updated your message {subject}")
            # message_form.save()
            return redirect('getMail-Address')
    
    context = {
        "form": message_form
    }
    
    return render(request, template_name='mForm.html', context=context)

@login_required(login_url="login")
def updateMail(request, pk):
    message = models.Message.objects.get(id=pk)
    message_form = forms.MessageForm(instance=message)
    
    if request.method == 'POST':
        message_form = forms.MessageForm(request.POST, instance=message)
        if message_form.is_valid():
            subject = message_form.cleaned_data['subject']
            message_form.save()
            messages.add_message(request, messages.INFO, f"You have successfully updated your message {subject}")
            return redirect('list-mail')
    
    context = {
        'form': message_form,
    }
    return render(request, template_name='mForm.html', context=context)


@login_required(login_url="login")
def deleteMail(request, pk):
    message = models.Message.objects.get(id=pk)
    if request.POST:
        message.delete()
    

@login_required(login_url="login")
def listAddress(request):
    address = models.EMails.objects.all()
    context = {
        'address': address
    }
    
    return render(request, template_name='list_adr.html', context=context)

@login_required(login_url="login")
def updateAddress(request, pk):
    address = models.EMails.objects.get(pk=pk)
    address_form = forms.EmailsForm(instance=address)
    
    if request.method == 'POST':
        address_form = forms.EmailsForm(request.POST, instance=address)
        if address_form.is_valid():
            address_form.save()
            return redirect('list-address')
    
    context = {
        'form':address_form,
    }
    
    return render(request, template_name='update_address.html', context=context)


def userRegister(request):
    form = forms.UserRegistrationForm()
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = form.save()
            messages.add_message(request, messages.INFO, f"You have been successfully registered as {username}")
            login(request, user)
            return redirect('getMail-Address')
    return render(request, template_name='register.html', context={'form': form})



def userLogin(request):
    form = AuthenticationForm()
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.INFO, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.add_message(request, messages.ERROR, "Invalid username or password.")
        else:
            messages.add_message(request, messages.ERROR, "Invalid username or password.")

    return render(request, template_name='login.html', context={"form":form})


def userLogout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("login")






MESSAGES = []


# Automatically send Mails on scheduled
def sendAutoMail():
    sender = 'tradevolatile@gmail.com'
    mails = models.Message.objects.all()
    adr = models.EMails.objects.all()
    user = models.User.objects.all()
    # print(user)
    # print(type(user))
    if user:
        for u in user:
            if not u.is_superuser:
                username = u.username
                if mails:
                    for mail in mails:
                        if mail.user == username: 
                            subject = mail.subject
                            message = mail.body
                            repeat_day = mail.schedule
                            
                            MESSAGES.append(
                                {
                                 "user": username,
                                 "message":[subject, subject, repeat_day]
                                }
                            )
                            
    if adr:
        for item in adr:
            if item.user == username:
                receiver = item.user
                
                mailSender(
                subject=subject, 
                message=message, 
                sender=sender, 
                receiver=receiver, 
                password=mail_pass
            )

                   
# sendAutoMail()