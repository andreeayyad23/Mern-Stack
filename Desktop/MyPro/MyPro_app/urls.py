from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('showall', views.showall),
    path('create', views.go_create),
    path('createshow', views.createshow),
    path('shows/<_id>', views.showone),
    path('shows/<_id>/edit', views.go_edit),
    path('shows/<_id>/update', views.editshow),
    path('delete/<_id>', views.delete_show),	   
	   
]