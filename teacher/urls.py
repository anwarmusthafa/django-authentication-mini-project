from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/', views.admin_login,name='admin_login'),
    path('admin_home/', views.admin_home,name='admin_home'),
    path('admin_logout/', views.admin_logout,name='admin_logout'),
    path('add_student/', views.add_student,name='add_student'),
    path('edit_student/<pk>', views.edit_student,name='edit_student'),
    path('delete_student/<pk>', views.delete_student,name='delete_student'),
    

    
]
