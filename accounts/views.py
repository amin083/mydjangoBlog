from django.contrib.auth.decorators import login_required
from . import models
from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms
from django.contrib.auth import login ,logout
from .models import Order
from .forms import OrderForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            #login
            return redirect('articles:list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #login user
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('user_profile/<user>')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method =='POST':
        logout(request)
        return redirect('articles:list')

def order_list(request, user):
    user = User.objects.get(username=user)  # Remove .username_validator
    orders = Order.objects.filter(user=user)
    return render(request, 'accounts/order_list.html', {'orders': orders})

def order_detail(request, title):
    #return HttpResponse(slug)
    accounts = models.Order.objects.get(title=title)
    return render(request, 'accounts/order_detail.html',{'accounts': accounts})

@login_required(login_url="/accounts/login")
def order_create(request):
    if request.method == 'POST':
        form = forms.OrderForm(request.POST, request.FILES)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.save()
            return redirect('accounts:list')
    else:
        form = forms.OrderForm()
    return render(request, 'accounts/order_create.html', {'form':form})

@login_required
def user_profile(request, user):
    return render(request, 'accounts/user_profile.html', {'user': user})

def history_view(request):
    return render(request, 'accounts/history.html')

def situation_view(request):
    return render(request, 'accounts/situation.html')


