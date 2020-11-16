from django.shortcuts import *
from django.http import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from admin_app.models import *

def Logout(request):
    logout(request)
    return redirect(reverse('login'))

def index(request):
    template_name="public/index.html"
    posts_list = posts.objects.all()
    events_list = events.objects.all()
    context={'posts_list':posts_list,'events_list':events_list}
    return render(request, template_name, context)

def Login(request):
    template_name="public/login.html"
    context={}
    return render(request,template_name,context)

def alumnae_dashboard(request):
    template_name="public/alumnae_dashboard.html"
    context={}
    return render(request,template_name,context)


def admin_dashboard(request):
    template_name="public/admin_dashboard.html"
    context={}
    return render(request,template_name,context)


def login_api(request):
    if request.method == "POST":
        email= request.POST.get('email')
        password=request.POST.get('password')
        data={}
        user = authenticate(request, username=email, password=password)
        if user is not None:
            data['user_exists']=True
            login(request,user)
            if request.user.is_staff:
                data['redirect_link']=reverse('admin_dashboard')
            else:
                data['redirect_link']=reverse('alumni_dashboard')
        else:
                data['user_exists']=False
    return JsonResponse(data)

def register(request):
    template_name="public/register.html"
    context={}
    return render(request,template_name,context)


def register_api(request):
    if request.method == "POST":
        fname= request.POST.get('fname')
        lname= request.POST.get('lname')
        email= request.POST.get('email')
        password=request.POST.get('password')
        qs_exists = User.objects.filter(username=email).exists()
        data = {"exists":True}
        if not qs_exists:
            data['exists']=False
            User_obj = User.objects.create_user(username=email,password=password,email=email)
            User_obj.first_name = fname
            User_obj.last_name = lname
            User_obj.save()
            alumnae_registration_obj = alumnae_registration()
            alumnae_registration_obj.user=User_obj
            alumnae_registration_obj.slug=unique_slug_generator(alumnae_registration_obj)
            alumnae_registration_obj.save()
            user = authenticate(request, username=email, password=password)
            login(request,User_obj)
            data['redirect_link']=reverse('alumni_dashboard')
        return JsonResponse(data)