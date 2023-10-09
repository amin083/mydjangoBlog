from django.contrib import admin
from .models import Order
from django.contrib.auth.models import User




class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'keyword']


admin.site.register(Order,OrderAdmin)

# Register your models here.
