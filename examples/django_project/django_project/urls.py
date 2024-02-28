from django.urls import path
from lists import views

urlpatterns = [
    path(r"", views.home_page, name="home"),
]
