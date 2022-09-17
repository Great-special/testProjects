from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.

MailingList = []
# Note that the method must be in Upper Case POST GET PUT
def index(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get("message")

        send_mail(
            subject,
            body,
            'tradevolatile@gmail.com',
            MailingList,
            fail_silently=False,
        )
        return redirect('mail form.html')
    return render(request, template_name='index.html')

def getEmails(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        MailingList.append(email)
        print(email, MailingList)
        
        context = {'emails':MailingList}
        return render(request, template_name='mail form.html', context=context)
    return render(request, template_name='mail form.html')