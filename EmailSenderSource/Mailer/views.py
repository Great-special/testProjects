from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.core.mail import send_mail
from  . import models, forms
from hidden import mail_pass
import smtplib
from email.message import EmailMessage


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
        
        msg = EmailMessage()
        msg.set_content(message)
        msg['subject'] = subject
        msg['to'] = receiver
        msg['from'] = sender
        
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, mail_pass)
        server.send_message(msg)
        
        server.quit()
        
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
    if request.method == 'POST':
        email = request.POST.get('email')
        MailingList.append(email)
        print(email, MailingList)
        
        for mail in MailingList:
            form = forms.EmailsForm(mail)
            if form.is_valid():
                form.save()
        
        context = {'emails':MailingList}
        return render(request, template_name='mail form.html', context=context)
    return render(request, template_name='mail form.html')



def listMail(request):
    messages = models.Message.objects.all()
    
    context = {
        'messages': messages
    }
    
    return render(request, template_name='list_mail.html', context=context)


def createMail(request):
    message_form = forms.MessageForm()
    if request.method == 'POST':
        message_form = forms.MessageForm(request.POST)
        if message_form.is_valid():
            message_form.save()
            return redirect('mail form.html')
    
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
            message_form.save()
            return redirect('list-mail')
        
    context = {
        'form': message_form,
    }
    
    return render(request, template_name='mForm.html', context=context)


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