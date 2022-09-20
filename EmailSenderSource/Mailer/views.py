from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from  . import models, forms

from hidden import mail_pass
from .alert import mailSender

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

def getEmails(request):
    if request.user.is_authenticated:
        user = request.user
    if request.method == 'POST':
        email = request.POST.get('email')
        MailingList.append(email)
        print(email, MailingList)
        
        for mail in MailingList:
            models.EMails.objects.create(email=mail, user=user)
            messages.add_message(request, messages.INFO, "your email address has been added")
        
        context = {'emails':MailingList}
        return render(request, template_name='mail form.html', context=context)
    else:
    
        return render(request, template_name='mail form.html')



def listMail(request):
    if request.user.is_authenticated:
        messages = models.Message.objects.filter(user=request.user)
    
    context = {
        'messages': messages
    }
    
    return render(request, template_name='list_mail.html', context=context)


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
  
    return render(request, template_name='mForm.html')


def deleteMail(request, pk):
    message = models.Message.objects.get(id=pk)
    if request.POST:
        message.delete()
    

def listAddress(request):
    address = models.EMails.objects.all()
    context = {
        'address': address
    }
    
    return render(request, template_name='list_adr.html', context=context)

def updateAddress(request, pk):
    address = models.EMails.objects.get(pk=pk)
    address_form = forms.EmailsForm(instance=address)
    
    if request.method == 'POST':
        address_form = forms.EmailsForm(request.POST, instance=address)
        if address_form.is_valid():
            address_form.save()
            return redirect('list-address')


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









# Automatically send Mails on scheduled
def sendAutoMail():
    mails = models.Message.objects.all()
    adr = models.EMails.objects.all()
    if adr:
        for item in adr:
            MailingList.append(item)
    print(MailingList)
    if mails:
        for mail in mails:
            if mail.schedule == 'Monday':
                print(mail.subject, mail.body)
                
                
# sendAutoMail()