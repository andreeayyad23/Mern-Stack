from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  # Define a basic route for the index view
    path('registration',views.registration),
    path('login',views.login),
    path('logout/', views.logout),
    path('trips/new/', views.go_create),
    path('dashboard', views.dashboard),
    path('createTrip', views.create_trip),
    path('trips/<int:_id>', views.details),
    path('delete/<_id>/', views.delete_trip),
    path('trips/<_id>/edit', views.edit),
    path('trips/<_id>/update', views.edit_trip),
    path('mytrips', views.my_trips, name='my_trips'),
    path('trips/<int:trip_id>/join', views.join_trip, name='join_trip'),
    path('trips/<int:trip_id>/leave', views.leave_trip, name='leave_trip'),

]