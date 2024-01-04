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

from django.contrib.auth import authenticate, login
from .forms import UploadFileForm
from docx import Document


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # login
            return redirect('accounts:user_profile')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # User login
            user = form.get_user()
            login(request, user)

            # Check if the user is a superuser
            if user.is_superuser:
                return redirect('accounts:admin_order_list')

            # Check if there's a 'next' parameter in the POST data
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('accounts:user_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:user_profile')


@login_required
def order_list(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'accounts/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    user = request.user
    order = models.Order.objects.get(id=order_id)
    if order.user == user.is_superuser:
       exit()
    else:
        return render(request, 'accounts/order_detail.html', {'order': order})
    return render(request, 'accounts/order_detail.html', {'order': order})
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


@login_required
def admin_order_list(request):
    order = Order.objects.all()
    return render(request, 'accounts/admin_order_list.html',{'orders':order})

def updat_customer(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # ذخیره فایل در دیسک
            uploaded_file = request.FILES['file']
            file_path = handle_uploaded_file(uploaded_file)

            # خواندن محتوای فایل Word
            document = Document(file_path)
            content = '\n'.join([paragraph.text for paragraph in document.paragraphs])

            # ارسال محتوا به قالب و یا انجام دیگر عملیات مورد نظر
            # در اینجا می‌توانید به عنوان مثال از content یا document استفاده کنید

            return render(request, 'result.html', {'content': content})
    else:
        form = UploadFileForm()
    return render(request, 'updat_cutomer.html', {'form': form})
def handle_uploaded_file(file):
    file_path = 'uploaded_files/' + file.name
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path

