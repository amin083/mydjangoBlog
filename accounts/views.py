from django.contrib.auth.decorators import login_required
from . import models
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms
from django.contrib.auth import login, logout
from .forms import OrderForm
from .models import Order
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # login
            return redirect('articles:list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # login user
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('accounts:user_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('articles:list')


@login_required
def order_list(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'accounts/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    user = request.user
    order = models.Order.objects.get(id=order_id)
    if order.user == user:
        return render(request, 'accounts/order_detail.html', {'order': order})
    return redirect('accounts:order_list')

@login_required
def order_create(request):
    if request.method == 'POST':
        form = forms.OrderForm(request.POST, request.FILES)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('accounts:order_list')
    else:
        form = forms.OrderForm()
    return render(request, 'accounts/order_create.html', {'form': form})


@login_required
def user_profile(request):
    return render(request, 'accounts/user_profile.html')


@login_required
def history_view(request):
    return render(request, 'accounts/history.html')


@login_required
def situation_view(request):
    return render(request, 'about.html')
