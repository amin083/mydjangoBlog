import os
import zipfile
from typing import io

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from docx import Document

from . import forms
from . import models
from .forms import DocumentForm, WordFileUploadForm_document
from .forms import OrderForm
from .models import Document
from .models import Order

from .forms import WordFileUploadForm

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
                return redirect('accounts:admin_profile')

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
def admin_profile(request):
    return render(request, 'accounts/admin_profile.html')


@login_required
def admin_order_list(request):
    if request.method == 'POST':
        order = Order.objects.get(pk=request.POST['order_id'])
        uploaded_file = request.FILES['uploaded_file']
        order.admin_uploade_file = uploaded_file
        order.save()
        return redirect('accounts:admin_order_list')
    else:
        orders = Order.objects.all()
        return render(request, 'accounts/admin_order_list.html', {'orders': orders})

@login_required
def delete_word_file(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order:
        if request.method == 'POST':
            # حذف فایل از آبجکت سفارش
            order.admin_uploade_file.delete()
            # ذخیره تغییرات
            order.save()
            return redirect('accounts:admin_order_list')

        return render(request, 'delete_word_file.html', {'order': order})


@login_required
def delete_word_file_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if document:
        if request.method == 'POST':
            # حذف فایل از آبجکت سفارش
            document.admin_uploade_file.delete()
            # ذخیره تغییرات
            document.save()
            return redirect('accounts:admin_document_list')

        return render(request, 'delete_word_file_document.html', {'document': document})

@login_required
def admin_download_file(request, order_id):
    order = Order.objects.get(pk=order_id)
    file_path = order.admin_uploade_file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename=order_{}.docx'.format(order.id)
            return response
    else:
        return HttpResponseNotFound('فایل هنوز اماده نشده')


@login_required
def admin_download_file_document(request, document_id):
    document = Document.objects.get(pk=document_id)
    file_path = document.admin_uploade_file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename=order_{}.docx'.format(document.id)
            return response
    else:
        return HttpResponseNotFound('فایل هنوز اماده نشده')

# @login_required
# def admin_document_list(request):
#     user = request.user
#     document = models.Document.objects.filter(user=user)
#
#     # Check if user has access to download the document
#     if document.user != user and not user.is_superuser:
#         return HttpResponseForbidden()
#
#     # Prepare file response
#     response = HttpResponse(document.uploaded_file.read(),
#                             content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#     response['Content-Disposition'] = f'attachment; filename={document.title}.docx'  # Set download filename
#
#     return response

@login_required
def admin_document_list(request):
    if request.method == 'POST':
        document = Document.objects.get(pk=request.POST['document_id'])
        uploaded_file = request.FILES['uploaded_file']
        document.uploaded_file = uploaded_file
        document.save()
        return redirect('accounts:admin_document_list')
    else:
        documents = Document.objects.all()
        return render(request, 'accounts/admin_document_list.html', {'documents': documents})

@login_required
def admin_upload_file(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = WordFileUploadForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('accounts:admin_order_list')

    else:
        form = WordFileUploadForm()

    return render(request, 'accounts/admin_upload_file.html', {'form': form, 'order': order})

@login_required
def admin_upload_file_document(request, document_id): #  برای ویراستاری بار گذاری ادمین
    document = get_object_or_404(Document, id=document_id)

    if request.method == 'POST':
        form = WordFileUploadForm_document(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('accounts:admin_document_list')

    else:
        form = WordFileUploadForm_document()

    return render(request, 'accounts/admin_upload_file_document.html', {'form': form, 'document': document})




@login_required
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # form.save()
            return redirect('accounts:document_list')
    else:
        form = DocumentForm()
    return render(request, 'accounts/upload_file.html', {'form': form})

def document_list(request): # for user
    user = request.user
    documents = Document.objects.filter(user=user)
    return render(request, 'accounts/document_list.html', {'documents': documents})

@login_required
def document_detail(request, document_id):
    user = request.user
    document = models.Document.objects.get(id=document_id)
    if document.user != user and not user.is_superuser:
        return HttpResponseForbidden()

    # Prepare file response
    response = HttpResponse(document.uploaded_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename={document.title}.docx'  # Set download filename

    return render(request, 'accounts/document_detail.html', {'document': document})


# @login_required
# def download_document(request, document_id):
#     user = request.user
#     document = get_object_or_404(Document, id=document_id)
#
#     # Check if user has access to download the document
#     if document.user != user and not user.is_superuser:
#         return HttpResponseForbidden()
#
#     # Prepare file response
#     response = HttpResponse(document.uploaded_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#     response['Content-Disposition'] = f'attachment; filename={document.title}.docx'  # Set download filename
#
#     return response