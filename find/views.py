from multiprocessing import context
from re import A
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Company, Job
from django.contrib.auth.models import Group
from django.contrib.auth.models import User,auth
from itertools import chain
import random
from .decoretor import *
# Create your views here.
def front(request):
    return render(request,'find/front.html')
@admin_only
@login_required(login_url='signin')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Company.objects.get(user=user_object)
    user_posts = Job.objects.filter(user=user_object)

    context={'user_profile':user_profile,'user_posts':user_posts}
    return render(request,'find/home.html',context)

@allowed_user(allowed_roles=['company'])
@login_required(login_url='signin')
def settings(request):
    user_profile = Company.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            name =  request.POST['name']
            email =  request.POST['email']
            main_location = request.POST['main_location']
            description = request.POST['description']
            user_profile.profileimg = image

            user_profile.name = name
            user_profile.email = email
            user_profile.main_location = main_location
            user_profile.description = description
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            name =  request.POST['name']
            email =  request.POST['email']
            main_location = request.POST['main_location']
            description = request.POST['description']

            user_profile.profileimg = image
            user_profile.name = name
            user_profile.email = email
            user_profile.main_location = main_location
            user_profile.description = description
            user_profile.save()
        return redirect('/')

    return render(request,'find/setting.html',{'user_profile':user_profile})

def signin(request):
    
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']


        user =auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalide')
            return redirect('signin')

    else:

        return render(request,'find/signin.html') 

@allowed_user(allowed_roles=['company'])
@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Job.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')

    else:
        return redirect('/')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@allowed_user(allowed_roles=['company'])
@login_required(login_url='signin')
def delete(request,pk):
    job = Job.objects.get(id=pk)
    job.delete()
    return redirect('/')

@login_required(login_url='signin')
def allJob(request):
    job = Job.objects.all()

    context ={'job':job}
    return render(request,'find/allJob.html',context)


def employee(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect('employee')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('employee')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                group = Group.objects.get(name='employee')
                user.groups.add(group)
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                return  redirect('allJob')

        else:
            messages.info(request,'password not matching')
            return redirect('employee')
        

    else:
        return render(request,'find/employeeSN.html')


def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                group = Group.objects.get(name='company')
                user.groups.add(group)
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)

                user_model=User.objects.get(username=username)
                new_profile=Company.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return  redirect('settings')

        else:
            messages.info(request,'password not matching')
            return redirect('signup')
        

    else:
        return render(request,'find/signup.html')