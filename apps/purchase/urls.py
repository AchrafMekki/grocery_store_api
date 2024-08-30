from django.urls import path
from . import views

app_name = 'purchase-urls'
urlpatterns = [
    path("cart/",views.view_cart,name='view_items'),
    path("new/", views.new_order, name='new_order'),
    path("get/", views.get_orders, name='get_orders'),
    path("get/<str:pk>/", views.get_order, name='get_order'),
    path("get/<str:pk>/process/", views.get_order, name='process_order'),
    path("get/<str:pk>/delete/", views.get_order, name='delete_order'),
    
   
]
