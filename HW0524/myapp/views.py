from os import name
from django.core import paginator
from django.shortcuts import get_object_or_404, redirect, render
from .models import Blog
from .forms import BlogForm, RegisterForm
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
# Create your views here.
def base(request):
    return render(request, 'base.html')

def home(request):
    blog = Blog.objects.all()
    paginator = Paginator(blog,3)
    page = request.GET.get('page')
    blog = paginator.get_page(page)
    return render(request, 'home.html', {'blog':blog})

def detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    return render(request, 'detail.html', {'blog':blog})

def new(request):
    form = BlogForm()
    return render(request, 'new.html', {'form':form})

def create(request):
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.pub_date = timezone.now()
        blog.save()
        return redirect('detail', blog.id)
    return redirect('home') 

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data= request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request = request, username = username, password = password)
            if(user is not None):
                login(request, user)
        return redirect('home')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
        return redirect('home')

    else:
        form = RegisterForm()
        return render(request, 'signup.html', {'form':form})