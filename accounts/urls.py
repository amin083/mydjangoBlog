from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns= [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('history/', views.history_view, name='history'),
    path('situation', views.situation_view, name='situation'),
    path('order_list/', views.order_list, name='order_list'),
    path('order/create/', views.order_create, name="create"),
    path('order/<int:order_id>/', views.order_detail, name="detail"),
    path('admin_order_list',views.admin_order_list,name='admin_order_list'),
    path('updat_customer',views.updat_customer, name= 'updat_customer'),

]
