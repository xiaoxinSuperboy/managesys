from django.urls import path
from apps.user import views
urlpatterns = [
    path('users/list/', views.user_list),
    path('users/add/', views.user_add),
    path('users/login/', views.user_login),
    path('users/add/model/', views.user_addmodel),
    path('users/edit/', views.user_edit),
    path('users/delete/', views.user_delete),
    path('users/logout/', views.user_logout),
    path('image/code/', views.image_code)
]