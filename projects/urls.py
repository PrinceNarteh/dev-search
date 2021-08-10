from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects),
    path('<int:pk>/', views.projects)
]
