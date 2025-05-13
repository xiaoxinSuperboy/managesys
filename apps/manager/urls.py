from django.urls import path
from apps.manager import views
urlpatterns = [
    path('admin/list/', views.admin_list),
    path('add/', views.admin_add),
    path('<int:nid>/edit/', views.admin_edit),
    path('<int:nid>/delete/', views.admin_delete),
    path('<int:nid>/reset/', views.reset),
]