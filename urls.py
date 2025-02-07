'''from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home-page'),
    
]'''
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns=[
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True),name='login'),
    path('userlogin', views.login_user, name="login-user"),
    path('user-register', views.registerUser, name="register-user"),
    path('logout/',views.logoutuser,name="logout"),
    path('profile',views.profile,name='profile'),
    path('update-profile',views.update_profile,name='update-profile'),
    path('update-password',views.update_password,name='update-password'),
    
    path('',views.home,name='home-page'),
    path('category',views.category_mgt,name='category-page'),
    path('manage_category',views.manage_category,name='manage-category'),
    path('save_category',views.save_category,name='save-category'),
    path('manage_category/<int:pk>',views.manage_category,name='manage-category-pk'),
    path('delete_category',views.delete_category,name='delete-category'),
     path('location',views.location_mgt,name='location-page'),
    path('manage_location',views.manage_location,name='manage-location'),
    path('save_location',views.save_location,name='save-location'),
    path('manage_location/<int:pk>',views.manage_location,name='manage-location-pk'),
    path('delete_location',views.delete_location,name='delete-location'),
 

]
