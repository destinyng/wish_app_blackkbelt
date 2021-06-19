from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('users/register', views.register),
    path('users/login', views.login),
    path('wishes', views.wishes),
    path('logout', views.logout),
    path('wishes/stats', views.stats),
    path('wishes/edit/<int:id>', views.edit),
    path('wishes/new', views.new),
    path('wishes/make_it_grant/<int:id>', views.make_it_grant),
    path('wishes/delete/<int:id>', views.delete),
    path('wishes/create', views.create),
    path('wishes/update/<int:id>', views.update),
    path('wishes/like/<int:id>', views.like)
]