from django.urls import path
from . import views

app_name = 'customer-urls'
urlpatterns = [
    path("register/", views.register, name="register-customer"),
    path("list/", views.get_list_customer, name="list-customer"),
    path("details/", views.get_current_user, name="current_user"),
    path("update/<int:pk>/", views.update_user_details, name="update_user"),
]
