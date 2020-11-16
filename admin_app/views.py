from django.shortcuts import *
from django.http import *
from django.http import *
from public.models import *
from django.core.files.storage import FileSystemStorage
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout

def register_alumni_api(request):
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

def register_alumni(request):
    template_name="admin_app/register.html"
    context={}
    return render(request,template_name,context)

def admin_dashboard(request):
    template_name="admin_app/admin_dashboard.html"
    context={}
    return render(request,template_name,context)

def manage_users(request):
    template_name="admin_app/manage_users.html"
    alumni_list = alumnae_registration.objects.all()
    context={'alumni_list':alumni_list}
    return render(request,template_name,context)

def delete_alumni_api(request):
    slug = request.POST.get("slug")  
    User.objects.filter(id=int(alumnae_registration.objects.get(slug=slug).user.id))
    return JsonResponse({"msg":"alumni deleted successfully"})

def post_event(request):
    template_name="admin_app/post_event.html"
    context={}
    return render(request,template_name,context)

def post_info(request):
    template_name="admin_app/post_info.html"
    context={}
    return render(request,template_name,context)

def post_info_api(request):
    title=request.POST.get('title')
    content = request.POST.get("content")
    picture = request.FILES['picture']
    fs = FileSystemStorage()
    filename = fs.save(picture.name, picture)
    file_url = fs.url(filename)
    posts_obj = posts()
    posts_obj.title=title
    posts_obj.content = content
    posts_obj.picture=filename
    posts_obj.save()
    return JsonResponse({"msg":"success"})



def post_event_api(request):
    title=request.POST.get('title')
    content = request.POST.get("content")
    events_obj = events()
    events_obj.title=title
    events_obj.venue = content
    events_obj.save()
    return JsonResponse({"msg":"success"})


