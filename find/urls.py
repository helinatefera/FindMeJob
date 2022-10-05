from django.urls import path
from . import views

urlpatterns = [
    path('',views.home ),
    path('front/',views.front,name='front'),
    path('employeeSN/',views.employee,name='employee'),
    path('allJob/',views.allJob,name='allJob'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('logout',views.logout,name='logout'),
    path('settings/',views.settings,name='settings'),
    path('upload',views.upload,name='upload'),
    path('delete/<str:pk>',views.delete,name='delete')
]