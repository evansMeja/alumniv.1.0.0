from django.shortcuts import *
from django.http import *
from .models import *
from public.models import *
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models import CharField, Value


def add_photo_to_gallery(request):
    if request.method == 'POST' and len(request.FILES) != 0:
        picture = request.FILES['picture']
        fs = FileSystemStorage()
        filename = fs.save(picture.name, picture)
        file_url = fs.url(filename)
        gallery_obj = photo_gallery()
        gallery_obj.picture = picture
        gallery_obj.user = request.user
        gallery_obj.save()
        return redirect(reverse("gallery"))

def save_mood(request):
    if request.method == 'POST':
        story_obj = story()
        if len(request.FILES) != 0:
            picture = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            file_url = fs.url(filename)
            story_obj.story_file = filename
            if file_url.endswith(".mp4"):
                story_obj.picture_present=False
                story_obj.video_present=True
            else:
                story_obj.picture_present=True
                story_obj.video_present=False

        share = request.POST.get("share")
        story_obj.content=share
        story_obj.user=request.user
        story_obj.save()
        Notifications_Obj = Notifications()
        Notifications_Obj.message="You have Successfully Shared A New Feed"
        Notifications_Obj.user= request.user
        Notifications_Obj.save()
        return redirect(reverse("alumni_dashboard"))

def alumni_public(request,slug):
    template_name="alumni/alumni_public.html"
    alumi_obi = alumnae_registration.objects.get(slug=slug)
    context={'alumi_obi':alumi_obi}
    return render(request,template_name,context)

def update_profile_api(request):
    if request.method == 'POST' and request.FILES['picture']:
        about=request.POST.get("about")
        phone=request.POST.get("phone")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")

        picture = request.FILES['picture']
        fs = FileSystemStorage()
        filename = fs.save(picture.name, picture)
        file_url = fs.url(filename)

        user_obj = request.user
        user_obj.first_name = first_name
        user_obj.last_name=last_name
        user_obj.save()
        alumnae_obj = alumnae_registration.objects.get(user=request.user)
        alumnae_obj.about=about
        alumnae_obj.phone=phone
        alumnae_obj.picture=filename
        alumnae_obj.save()
        return JsonResponse({"test":"test"})

def fetch_fields_api(request):
    course_id= request.GET.get("course_id")
    fields = field.objects.filter(course=courses.objects.get(id=int(course_id)))
    return JsonResponse(fields,safe=False)

def profile(request):
    template_name="alumni/profile.html"
    alumnae_obj = alumnae_registration.objects.get(user=request.user)
    courses_list = courses.objects.all()
    context={'alumnae_obj':alumnae_obj,'courses_list':courses_list}
    return render(request,template_name,context)

def followers(request):
    template_name="alumni/followers.html"

    cur_user_followers = []
    alumni_list= alumnae_registration.objects.all().exclude(user=request.user)
    for alumni in alumni_list:
        test_alumni_obj = alumnae_registration.objects.get(user=alumni.user)
        if test_alumni_obj.followers.filter(id=request.user.pk).exists():
           cur_user_followers.append(alumni)
    context={'alumni_list':cur_user_followers}
    return render(request,template_name,context)




def unfollow_api(request):
    alumni_id = request.POST.get("alumni")
    user_obj_to_follow = User.objects.get(id=int(alumni_id))
    current_alumni_obj = alumnae_registration.objects.get(user=request.user)
    data = {}
    qs_exists = current_alumni_obj.followers.filter(id=user_obj_to_follow.pk).exists()
    if qs_exists:
        data['msg']="unfollowed"
        current_alumni_obj.followers.remove(user_obj_to_follow)
        current_alumni_obj.save()
    else:
        data['msg']="already unfollowed"
    return JsonResponse(data)

def follow_api(request):
    alumni_id = request.POST.get("alumni")
    user_obj_to_follow = User.objects.get(id=int(alumni_id))
    current_alumni_obj = alumnae_registration.objects.get(user=request.user)
    data = {}
    qs_exists = current_alumni_obj.followers.filter(id=user_obj_to_follow.pk).exists()
    if qs_exists:
        data['msg']="user already saved"
    else:
        data['msg']="ready to save"
        current_alumni_obj.followers.add(user_obj_to_follow)
        current_alumni_obj.save()
    return JsonResponse(data)


def follow(request):
    template_name="alumni/follow.html"
    current_alumni_obj = alumnae_registration.objects.get(user=request.user)
    alumni_list= alumnae_registration.objects.all().exclude(user=request.user)

    #print("initial length "+str(len(alumni_list)))
    c=0
    unfollowed_alumnis = []
    for alumni in alumni_list:
        if not current_alumni_obj.followers.filter(id=alumni.user.pk).exists():
            unfollowed_alumnis.append(alumni)
            c= c+1

    #print("final length "+str(c))

    context={'alumni_list':unfollowed_alumnis}
    return render(request,template_name,context)


def follow_api(request):
    alumni_id = request.POST.get("alumni")
    user_obj_to_follow = User.objects.get(id=int(alumni_id))
    current_alumni_obj = alumnae_registration.objects.get(user=request.user)
    data = {}
    qs_exists = current_alumni_obj.followers.filter(id=user_obj_to_follow.pk).exists()
    if qs_exists:
        data['msg']="user already saved"
    else:
        data['msg']="ready to save"
        current_alumni_obj.followers.add(user_obj_to_follow)
        current_alumni_obj.save()
    return JsonResponse(data)


def like_post(request):
    post_id = request.POST.get("post_id")
    story_obj = story.objects.get(id=int(post_id))
    qs_exists = story_obj.likes.filter(id=request.user.pk).exists()
    if qs_exists:
        story_obj.likes.remove(request.user)
    else:
        story_obj.likes.add(request.user)
    story_obj.save()
    is_liking = story_obj.likes.filter(id=request.user.pk).exists()
    return JsonResponse({'likes':story_obj.likes.count(),'is_liking':is_liking})

def new_comment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        post_id = request.POST.get('post_id')

        story_object = story.objects.get(id=int(post_id))

        new_comment = comments()
        new_comment.content = comment 
        new_comment.story = story_object
        new_comment.save()
        qs = list(comments.objects.filter(story=story_object).values())
        return JsonResponse(qs,safe=False)


def fetch_comments_endpoint(request):
    post_id = request.POST.get("post_id")
    story_obj = story.objects.get(id=int(post_id))
    qs = list(comments.objects.filter(story=story_obj).values())
    return JsonResponse(qs,safe=False)

def heart_post(request):
    post_id = request.POST.get("post_id")
    story_obj = story.objects.get(id=int(post_id))
    qs_exists = story_obj.hearts.filter(id=request.user.pk).exists()
    if qs_exists:
        story_obj.hearts.remove(request.user)
    else:
        story_obj.hearts.add(request.user)
    story_obj.save()
    return JsonResponse({'hearts':story_obj.hearts.count()})




def all_feeds(request):
    template_name="alumni/all_feeds.html"
    story_list = story.objects.all()
    alumni_list= alumnae_registration.objects.all().exclude(user=request.user)
    notifications_list = Notifications.objects.filter(user=request.user)
    alumni_obj = alumnae_registration.objects.get(user=request.user)

    f = []
    for s in story_list:
        d={}
        d['info'] = s
        d['is_liking'] = s.likes.filter(id=request.user.pk).exists()
        d['is_hearting'] = s.hearts.filter(id=request.user.pk).exists()
        f.append(d)
    context={'story_list':f,'alumni_list':alumni_list,"alumni_obj":alumni_obj,'notifications_list':notifications_list,'f':f}

    return render(request,template_name,context)


def following(request):
    template_name="alumni/following.html"
    current_alumni_obj = alumnae_registration.objects.get(user=request.user)
    alumni_list= alumnae_registration.objects.all().exclude(user=request.user)

    #print("initial length "+str(len(alumni_list)))
    c=0
    unfollowed_alumnis = []
    for alumni in alumni_list:
        if current_alumni_obj.followers.filter(id=alumni.user.pk).exists():
            unfollowed_alumnis.append(alumni)
            c= c+1

    #print("final length "+str(c))

    context={'alumni_list':unfollowed_alumnis}
    return render(request,template_name,context)

    

def connect_friends(request,slug):
    template_name="alumni/following_friends.html"
    alumni_list= alumnae_registration.objects.all().exclude(user=request.user)
    curr_user_instance = User.objects.get(id=int(slug))
    current_alumni_obj = alumnae_registration.objects.get(user=curr_user_instance)
    alumni_obj = alumnae_registration.objects.get(user=request.user)


    c=0
    followed_alumnis = []
    for alumni in alumni_list:
        if not current_alumni_obj.followers.filter(id=alumni.user.pk).exists():
            followed_alumnis.append(alumni)
            c= c+1

    context={'alumni_list':followed_alumnis,"alumni_obj":alumni_obj,"slug":slug}
    return render(request,template_name,context)



def folowers_friends(request,slug):
    template_name="alumni/following_friends.html"
    alumni_list= alumnae_registration.objects.all().exclude(user=request.user)
    curr_user_instance = User.objects.get(id=int(slug))
    current_alumni_obj = alumnae_registration.objects.get(user=curr_user_instance)
    alumni_obj = alumnae_registration.objects.get(user=request.user)


    cur_user_followers = []
    alumni_list= alumnae_registration.objects.all().exclude(user=request.user)
    for alumni in alumni_list:
        test_alumni_obj = alumnae_registration.objects.get(user=alumni.user)
        if test_alumni_obj.followers.filter(id=current_alumni_obj.pk).exists():
           cur_user_followers.append(alumni)

    context={'alumni_list':cur_user_followers,"alumni_obj":alumni_obj,"slug":slug}
    return render(request,template_name,context)

def following_friends(request,slug):
    template_name="alumni/following_friends.html"
    alumni_list= alumnae_registration.objects.all().exclude(user=request.user)
    curr_user_instance = User.objects.get(id=int(slug))
    current_alumni_obj = alumnae_registration.objects.get(user=curr_user_instance)
    alumni_obj = alumnae_registration.objects.get(user=request.user)

    c=0
    followed_alumnis = []
    for alumni in alumni_list:
        if current_alumni_obj.followers.filter(id=alumni.user.pk).exists():
            followed_alumnis.append(alumni)
            c= c+1
    context={'alumni_list':followed_alumnis,"alumni_obj":alumni_obj,"slug":slug}
    return render(request,template_name,context)


def alumni_dashboard(request):
    return redirect(reverse("all_feeds"))


def gallery(request):
    template_name="alumni/gallery.html"
    gallery_list = photo_gallery.objects.filter(user=request.user)
    context={'gallery_list':gallery_list}
    return render(request,template_name,context)


def my_photos(request,slug):
    template_name="alumni/my_photos.html"
    alumni_obj = alumnae_registration.objects.get(user=request.user)
    user_obj = User.objects.get(id=int(slug))
    gallery_list = photo_gallery.objects.filter(user=user_obj)
    context={'gallery_list':gallery_list,'user_obj':user_obj,"slug":slug,'alumni_obj':alumni_obj}
    return render(request,template_name,context)

def about(request,slug):
    template_name="alumni/about.html"
    story_list = story.objects.all()
    user_obj = User.objects.get(id=int(slug))
    alumni_list= alumnae_registration.objects.all().exclude(user=request.user).filter(user=user_obj)
    alumni_obj = alumnae_registration.objects.get(user=request.user)
    context={'story_list':story_list,'alumni_list':alumni_list,"alumni_obj":alumni_obj,"slug":slug}
    return render(request,template_name,context)


def user_profile(request,slug):
    template_name="alumni/feed_detail.html"
    user_obj = User.objects.get(id=int(slug))
    story_list = story.objects.filter(user=user_obj)
    alumni_list= alumnae_registration.objects.all().exclude(user=request.user).filter(user=user_obj)
    alumni_obj = alumnae_registration.objects.get(user=request.user)
    context={'story_list':story_list,'alumni_list':alumni_list,"alumni_obj":alumni_obj,"slug":slug}
    return render(request,template_name,context)


def notification_endpoint(request):
    notifications_list = list(Notifications.objects.filter(user=request.user).values())
    return JsonResponse({'notifications':notifications_list},safe=False)


# def alumni_dashboard(request):
#     template_name="alumni/alumni_dashboard.html"
#     story_list = story.objects.all()
#     alumni_list= alumnae_registration.objects.all().exclude(user=request.user)
#     alumni_obj = alumnae_registration.objects.get(user=request.user)
#     context={'story_list':story_list,'alumni_list':alumni_list,"alumni_obj":alumni_obj}
#     return render(request,template_name,context)


def post_story(request):
    content=request.POST.get('content')
    story_obj = story()
    story_obj.user = request.user
    story_obj.content=content
    story_obj.save()
    return JsonResponse({"msg":"success"})

def alumni_detail(request,slug):
    template_name="alumni/alumni_detail.html"
    alumnae_registration_obj = alumnae_registration.objects.get(slug=slug)
    messages_table_list = []
    messages_table_list_all =  messages_table.objects.all()

    c = (len(messages_table_list_all) - 1)
    i = 0
    while c > 0:
        if messages_table_list_all[c].sender == request.user and messages_table_list_all[c].receiver == alumnae_registration_obj.user:
            mydict={"msg":messages_table_list_all[c],'type':'user1'}
            messages_table_list.append(mydict)
            i = i + 1
        elif messages_table_list_all[c].receiver == request.user and messages_table_list_all[c].sender == alumnae_registration_obj.user:
            mydict={"msg":messages_table_list_all[c],'type':'user2'}
            i = i + 1
            messages_table_list.append(mydict)
        if i > 4:
            break
            
        c = c - 1

    # for msg in messages_table_list_all:
    #     if msg.sender == request.user and msg.receiver == alumnae_registration_obj.user or msg.receiver == request.user and msg.sender == alumnae_registration_obj.user:
    #         messages_table_list.append(msg)
    #print(messages_table_list)
    context={'alumnae_registration_obj':alumnae_registration_obj,'messages_table_list':messages_table_list}
    return render(request,template_name,context)

def send_message(request):
    sender_id = request.POST.get("sender")
    receiver_id = request.POST.get("receiver")
    content = request.POST.get("content")
    messages_table_obj = messages_table()
    messages_table_obj.sender= User.objects.get(id=int(sender_id))
    messages_table_obj.receiver= User.objects.get(id=int(receiver_id))
    messages_table_obj.content=content
    messages_table_obj.save()
    return JsonResponse({"msg":"success"})