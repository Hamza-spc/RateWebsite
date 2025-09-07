from django.urls import path
from . import views

app_name = 'venues'

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # Venue listing and search
    path('venues/', views.venue_list, name='venue_list'),
    path('venues/search/', views.venue_search, name='venue_search'),
    path('venues/category/<slug:category_slug>/', views.venue_list_by_category, name='venue_list_by_category'),
    
    # Venue details
    path('venue/<slug:venue_slug>/', views.venue_detail, name='venue_detail'),
    
    # Rating and reviews
    path('venue/<slug:venue_slug>/rate/', views.rate_venue, name='rate_venue'),
    
    # Admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/category/<slug:category_slug>/', views.admin_venues_by_category, name='admin_venues_by_category'),
    path('admin-dashboard/category/<slug:category_slug>/edit/', views.admin_edit_venues, name='admin_edit_venues'),
    path('admin-dashboard/category/<slug:category_slug>/bulk-action/', views.admin_bulk_action, name='admin_bulk_action'),
    path('admin-dashboard/add-venue/', views.add_venue, name='add_venue'),
    path('admin-dashboard/edit-venue/<int:venue_id>/', views.edit_venue, name='edit_venue'),
    path('admin-dashboard/delete-venue/<int:venue_id>/', views.delete_venue, name='delete_venue'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # About
    path('about/', views.about, name='about'),
]
