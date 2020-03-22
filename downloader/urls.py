from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('drama/', views.drama_index, name='Drama Index'),
    path('drama/show/<str:link>', views.drama_show, name='Drama Show'),
    path('drama/download/<str:link>', views.drama_download, name='Drama Download')
]
