from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_designs, name='search'),
    path('create/', views.create_design, name='create-design'),
]
