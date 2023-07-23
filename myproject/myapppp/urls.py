from django.urls import path
from . import views

urlpatterns=[
    path('', views.index,name='index'),
    path('context.html',views.context,name='context')
]