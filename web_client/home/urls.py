from django.conf.urls import url
from . import views

urlpatterns = [
    url('about/', views.about, name="aboutpage"),
    url('', views.home, name="homepage"),
]