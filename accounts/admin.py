from django.contrib import admin
from .models import Order
from .models import Document
from django.contrib.auth.models import User


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'keyword', 'admin_uploade_file']


admin.site.register(Order, OrderAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'uploaded_file', 'admin_uploade_file']


admin.site.register(Document, DocumentAdmin)
# Register your models here.
