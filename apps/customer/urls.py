from django.urls import path
from . import views

app_name = 'product-url'
urlpatterns = [
    path("register/", views.register, name="register-customer"),
    path("me/", views.current_user, name="current_user"),
    path("me/update/", views.update_user, name="current_user"),

]
