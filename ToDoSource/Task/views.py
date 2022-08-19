import datetime
import pytz
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from . import forms

# Create your views here.

def home(request):
    tasks = models.Tasks.objects.all()
    print(tasks)
    
    while True:
        # print(pytz.all_timezones) # list of time zones  .strftime("%Y-%m-%d %H:%M:%S")
    
        tz = pytz.timezone('Africa/Lagos')
        na = datetime.datetime.utcnow()
        na_aware = tz.localize(na)
        info = "None"
        for task in tasks:
            sch = task.schedule
            if sch == na_aware:
                info = "Task scheduled"
                print(info)
        
        context = {
            'tasks': tasks,
            'info': info,
            }
        return render(request, "task/home.html", context)




def add(request):
    form = forms.TasksForm()
    # checking if the user has submitted the form
    if request.method == 'POST':
        form = forms.TasksForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {
        'form': form, 
    }
    return render(request, "task/create.html", context)
        
def update_task(request, id):
    
    task = models.Tasks.objects.get(id = id)
    
    form = forms.TasksForm(instance = task)
    
    if request.method == 'POST':
        form = forms.TasksForm(request.POST, instance = task)
        if form.is_valid():
            form.save()
        return redirect('/')
    
    context = {
        'form': form, 
    }
    return render(request, 'task/edit.html', context)


def delete_task(request, id):
    task = models.Tasks.objects.get(id = id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    
    context = {
        'item': task
        }
    
    return render(request, 'task/delete.html', context)