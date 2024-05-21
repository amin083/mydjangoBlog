from django.urls import path
from . import views
from .views import upload_file


app_name = 'accounts'
urlpatterns= [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('history/', views.history_view, name='history'),
    path('order_list/', views.order_list, name='order_list'),
    path('order/create/', views.order_create, name="create"),
    path('order/<int:order_id>/', views.order_detail, name="detail"),
    path('admin_order_list',views.admin_order_list, name='admin_order_list'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('document_list/', views.document_list, name='document_list'),
    path('admin', views.admin_profile, name='admin_profile'),
    path('admin_document_list', views.admin_document_list, name='admin_document_list'),
    path('document_detail/<int:document_id>', views.document_detail, name='document_detail'),
    path('admin_download_file/<int:order_id>', views.admin_download_file, name='admin_download_file'),
    path('admin_download_file_document/<int:document_id>', views.admin_download_file_document, name='admin_download_file_document'),
    path('admin_upload_file/<int:order_id>', views.admin_upload_file, name='admin_upload_file'),
    path('delete_word_file/<int:order_id>', views.delete_word_file, name='delete_word_file'),
    path('delete_word_file_document/<int:document_id>', views.delete_word_file_document, name='delete_word_file_document'),
    path('admin_upload_file_document/<int:document_id>', views.admin_upload_file_document, name='admin_upload_file_document'),

]
