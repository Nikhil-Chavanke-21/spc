"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from users import views as user_views
from files.api import views as api_views

urlpatterns = [
    url('admin/', admin.site.urls),
    url('home/', include('home.urls')),
    url('register/', user_views.register, name='register'),
    url('my-cloud/', user_views.my_cloud, name='my_cloud'),
    url('scheme/', user_views.scheme, name='scheme'),    
    #url('my_login/', user_views.my_login, name='my_login'),
    url(r'^login/$', user_views.DLoginView.as_view(template_name='users/login.html'), name='login'),
    url('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    url('files/', include('files.api.urls')),
]