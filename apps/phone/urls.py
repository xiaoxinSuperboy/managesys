from django.urls import path
from apps.phone import views

urlpatterns = [
    path('numlist/', views.num_list),
    path('add/', views.num_add),
    path('<int:nid>/edit/', views.edit_num),
    path('<int:nid>/delete/', views.delete_num),
]