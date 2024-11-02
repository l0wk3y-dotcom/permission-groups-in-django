from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from .forms import RegisterForm, PostForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from .models import *

@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()
    for post in posts:
        post.author.is_banned = post.author.groups.filter(name="banned").exists()
    return render(request, "home.html", {"posts":posts})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            default_group, created = Group.objects.get_or_create(name="default")
            user.groups.add(default_group)
            login(request,user)
            return redirect("/posts/home")
    else:
        form = RegisterForm()
    return render(request,"registration/register.html",{"form":form})
    

@permission_required("Posts.add_post",login_url="/login", raise_exception=True)
@login_required(login_url="/login")
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/posts/home")
    else:
        form = PostForm()
        return render(request, "create_post.html", {"form" : form})
    
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user or not request.user.has_perm("Posts.delete_post"):
        return HttpResponseForbidden("You are not allowed to delete this post.")
    post.delete()
    return redirect('/posts/home')  # Redirect to the home page or wherever you want after deletion

def ban_user(request, pk):
    if request.user.is_staff:
        print(f"id is being passed as {pk}")
        user = get_object_or_404(User, pk=pk)
        user.groups.clear()
        banned_group, created = Group.objects.get_or_create(name="banned")
        user.groups.add(banned_group)
        return redirect("/posts/home")
    else:
        return HttpResponseForbidden("you do not have permission to ban users")
