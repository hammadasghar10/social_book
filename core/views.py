from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse
@login_required(login_url='signin')
def index (request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        posts=Post.objects.all()
    except Profile.DoesNotExist:
      
        return redirect("signin")
    
    return render(request, 'index.html', {'user_profile': user_profile,'posts':posts,
                                          })
@login_required(login_url='signin')
def upload(request):
   if request.method=="POST":
      user=request.user.username
      image=request.FILES.get("image_upload")
      caption=request.POST["caption"]
      new_post=Post.objects.create(user=user,image=image,caption=caption)
      new_post.save()
      return redirect("/")
      
   else:
      return redirect("signin")
@login_required(login_url='signin')
def like_post(request):
      username=request.user.username
      post_id=request.GET.get('post_id')
      post=Post.objects.get(id=post_id)
      like_filter=LikePost.objects.filter(username=username,post_id=post_id).first()
      if like_filter==None:
         new_like=LikePost.objects.create(post_id=post_id,username=username)
         new_like.save()
         post.no_of_likes=post.no_of_likes+1
         post.save()
         return redirect('/')
      else:
         like_filter.delete()
         post.no_of_likes=post.no_of_likes-1
         post.save()
         return redirect('/')

@login_required(login_url="signin")
def profile(request,pk):
   user_profile = Profile.objects.get(user__username=pk)
   user_posts=Post.objects.filter(user=pk)
   user_post_length=len(user_posts)
   return render(request,"profile.html",context={"user_profile":user_profile,
                                                 "user_posts":user_posts,
                                                 "user_post_length":user_post_length})
@login_required(login_url="signin")
def setting(request):
   user_profile=Profile.objects.get(user=request.user)
   if request.method=="POST":

      if request.FILES.get("image") == None:
         image=user_profile.profileimg
         bio=request.POST['bio']
         location=request.POST['location']
         user_profile.profileimg=image
         user_profile.bio=bio
         user_profile.location=location
         user_profile.save()
      elif request.FILES.get("image")!=None:
         image=request.FILES.get('image')
         bio=request.POST['bio']
         location=request.POST['location']
         user_profile.profileimg=image
         user_profile.bio=bio
         user_profile.location=location
         user_profile.save()
      return redirect('setting')
         
   return render(request,"setting.html",{"user_profile":user_profile})
def signup(request):
    if request.method=='POST':
      username=request.POST['username']
      email=request.POST["email"]
      password=request.POST['password']
      password2=request.POST['password']
      if password==password2:
         if User.objects.filter(email=email).exists():
            messages.info(request,"Email already using ")
            return redirect("signup")
         elif User.objects.filter(username=username).exists():
            messages.info(request,"username already taken")
            return redirect("signup")
         else:
           user=User.objects.create_user(username=username,email=email,password=password)     
           user.save() 
           #log user in and redirect to setting page
           user_login=auth.authenticate(username=username,password=password)
           auth.login(request,user_login)
           #create a user profile object
           user_model=User.objects.get(username=username)
           new_profile=Profile.objects.create(user=user_model)
           new_profile.save()
           return redirect('setting')
      else:
         messages.info(request, 'passward is wrong ')
         return redirect('signup')
         
    else:
     return render(request,'signup.html')
def signin(request):
   if request.method =='POST':
      username=request.POST['username']
      password=request.POST['password']
      user=auth.authenticate(username=username,password=password)
      if user is not None:
         auth.login(request,user)
         return redirect('index')
      else:
         messages.info(request,"invalid Credentials ")
         return redirect('signin')

   else:
    return render(request,'signin.html')
@login_required(login_url='signin')
def logout(request):
   auth.logout(request)
   return redirect('signin')
@login_required(login_url='sigin')
def follow(request):
 if request.metho=="POST":
    follower=request.POST['follower']
    user=request.POST['user']
    if followercount.objects.filter(follower=follower,user=user).first():
       delete_follower=followercount.objects.get(follower=follower,user=user)
       delete_follower.delete()
       return redirect('/profile/'+user)
    else:
       new_follower=followercount.objects.create(follower=follower,user=user)
       new_follower.save()
 else:
    return redirect('/')