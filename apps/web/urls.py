from django.urls import path
from apps.web import views
urlpatterns = [
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete,),
    path('depart/edit/', views.depart_edit),
]