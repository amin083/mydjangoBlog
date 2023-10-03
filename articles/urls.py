from django.urls import path
from . import views

app_name= "articles"
urlpatterns = [
    path('', views.articles_list, name="list"),
    path('create', views.create_article, name="create"),
    path('<slug>', views.articles_detail, name="detail"),

]
