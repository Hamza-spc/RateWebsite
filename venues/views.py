from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Venue, Category, Rating, ContactMessage, Statistics
from .forms import VenueForm, ContactForm, RatingForm


def home(request):
    """Homepage with video background and search functionality"""
    # Get statistics
    stats = Statistics.get_or_create_stats()
    
    # Get featured venues
    featured_venues = Venue.objects.filter(is_active=True, is_featured=True)[:6]
    
    # Get categories for the search form
    categories = Category.objects.all()
    
    context = {
        'featured_venues': featured_venues,
        'categories': categories,
        'stats': stats,
    }
    return render(request, 'venues/home.html', context)


def venue_list(request):
    """List all venues with filtering and pagination"""
    venues = Venue.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        venues = venues.filter(category__slug=category_slug)
    
    # Filter by city
    city = request.GET.get('city')
    if city:
        venues = venues.filter(city__icontains=city)
    
    # Filter by search query
    search_query = request.GET.get('search')
    if search_query:
        venues = venues.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(country__icontains=search_query)
        )
    
    # Order by rating (highest first)
    venues = venues.order_by('-average_rating', '-total_ratings')
    
    # Pagination
    paginator = Paginator(venues, 12)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'venues': venues,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
        'city_filter': city,
    }
    return render(request, 'venues/venue_list.html', context)


def venue_search(request):
    """Handle search requests"""
    if request.method == 'GET':
        search_query = request.GET.get('q', '')
        category = request.GET.get('category', '')
        location = request.GET.get('location', '')
        
        venues = Venue.objects.filter(is_active=True)
        
        if search_query:
            venues = venues.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(country__icontains=search_query)
            )
        
        if category:
            venues = venues.filter(category__slug=category)
        
        if location:
            venues = venues.filter(
                Q(city__icontains=location) |
                Q(country__icontains=location)
            )
        
        venues = venues.order_by('-average_rating', '-total_ratings')
        
        context = {
            'venues': venues,
            'search_query': search_query,
            'category_filter': category,
            'location_filter': location,
        }
        return render(request, 'venues/search_results.html', context)
    
    return redirect('venues:venue_list')


def venue_list_by_category(request, category_slug):
    """List venues by category"""
    category = get_object_or_404(Category, slug=category_slug)
    venues = Venue.objects.filter(is_active=True, category=category).select_related('category').prefetch_related('images')
    
    # Apply additional filters
    city = request.GET.get('city')
    if city:
        venues = venues.filter(city__icontains=city)
    
    search_query = request.GET.get('search')
    if search_query:
        venues = venues.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    venues = venues.order_by('-average_rating', '-total_ratings')
    
    # Pagination
    paginator = Paginator(venues, 12)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'venues': venues,
        'category': category,
        'categories': categories,
        'search_query': search_query,
        'city_filter': city,
    }
    return render(request, 'venues/venue_list.html', context)


def venue_detail(request, venue_slug):
    """Detailed view of a venue"""
    venue = get_object_or_404(Venue, slug=venue_slug, is_active=True)
    
    # Get ratings and reviews
    ratings = venue.ratings.all().select_related('user').order_by('-created_at')
    
    # Get nearby venues (same city, different venue)
    nearby_venues = Venue.objects.filter(
        is_active=True,
        city=venue.city
    ).exclude(id=venue.id)[:6]
    
    # Check if user has already rated this venue
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = venue.ratings.get(user=request.user)
        except Rating.DoesNotExist:
            pass
    
    context = {
        'venue': venue,
        'ratings': ratings,
        'nearby_venues': nearby_venues,
        'user_rating': user_rating,
    }
    return render(request, 'venues/venue_detail.html', context)


@login_required
def rate_venue(request, venue_slug):
    """Rate a venue"""
    venue = get_object_or_404(Venue, slug=venue_slug, is_active=True)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            comment = form.cleaned_data.get('comment', '')
            
            # Create or update rating
            rating, created = Rating.objects.get_or_create(
                venue=venue,
                user=request.user,
                defaults={'rating': rating_value, 'comment': comment}
            )
            
            if not created:
                rating.rating = rating_value
                rating.comment = comment
                rating.save()
            
            # Update venue statistics
            venue.update_rating_stats()
            
            messages.success(request, 'Thank you for your rating!')
            return redirect('venues:venue_detail', venue_slug=venue.slug)
    else:
        # Pre-fill form if user already rated
        try:
            existing_rating = venue.ratings.get(user=request.user)
            form = RatingForm(initial={
                'rating': existing_rating.rating,
                'comment': existing_rating.comment
            })
        except Rating.DoesNotExist:
            form = RatingForm()
    
    context = {
        'venue': venue,
        'form': form,
    }
    return render(request, 'venues/rate_venue.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard for managing venues"""
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('venues:home')
    
    # Get all categories
    categories = Category.objects.all().annotate(venue_count=Count('venues'))
    
    # Get statistics
    stats = Statistics.get_or_create_stats()
    
    context = {
        'categories': categories,
        'stats': stats,
    }
    return render(request, 'venues/admin_dashboard.html', context)


@login_required
def add_venue(request):
    """Add a new venue (admin only)"""
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('venues:home')
    
    # Get category from URL parameter
    category_slug = request.GET.get('category')
    initial_data = {}
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            initial_data['category'] = category.id
        except Category.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.save()
            
            # Handle multiple images
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                VenueImage.objects.create(
                    venue=venue,
                    image=image,
                    order=i
                )
            
            # Update statistics
            stats = Statistics.get_or_create_stats()
            stats.update_all_stats()
            
            messages.success(request, f'Venue "{venue.name}" has been added successfully!')
            
            # Redirect back to category view if coming from there
            if category_slug:
                return redirect('venues:admin_venues_by_category', category_slug=category_slug)
            else:
                return redirect('venues:admin_dashboard')
    else:
        form = VenueForm(initial=initial_data)
    
    context = {
        'form': form,
        'category_slug': category_slug,
    }
    return render(request, 'venues/add_venue.html', context)


@login_required
def edit_venue(request, venue_id):
    """Edit a venue (admin only)"""
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('venues:home')
    
    venue = get_object_or_404(Venue, id=venue_id)
    
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            
            # Handle new images
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                VenueImage.objects.create(
                    venue=venue,
                    image=image,
                    order=venue.images.count() + i
                )
            
            messages.success(request, f'Venue "{venue.name}" has been updated successfully!')
            return redirect('venues:admin_dashboard')
    else:
        form = VenueForm(instance=venue)
    
    context = {
        'form': form,
        'venue': venue,
    }
    return render(request, 'venues/edit_venue.html', context)


@login_required
def delete_venue(request, venue_id):
    """Delete a venue (admin only)"""
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('venues:home')
    
    venue = get_object_or_404(Venue, id=venue_id)
    
    if request.method == 'POST':
        venue_name = venue.name
        venue.delete()
        
        # Update statistics
        stats = Statistics.get_or_create_stats()
        stats.update_all_stats()
        
        messages.success(request, f'Venue "{venue_name}" has been deleted successfully!')
        return redirect('venues:admin_dashboard')
    
    context = {
        'venue': venue,
    }
    return render(request, 'venues/delete_venue.html', context)


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('venues:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'venues/contact.html', context)


def about(request):
    """About page"""
    stats = Statistics.get_or_create_stats()
    
    context = {
        'stats': stats,
    }
    return render(request, 'venues/about.html', context)


@login_required
def admin_venues_by_category(request, category_slug):
    """Admin view for venues by category"""
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('venues:home')
    
    category = get_object_or_404(Category, slug=category_slug)
    venues = Venue.objects.filter(category=category).select_related('category').prefetch_related('images')
    
    # Apply search filter
    search_query = request.GET.get('search')
    if search_query:
        venues = venues.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(country__icontains=search_query)
        )
    
    venues = venues.order_by('-created_at')
    
    # Get statistics for this category
    active_venues = venues.filter(is_active=True)
    featured_venues = venues.filter(is_featured=True)
    total_ratings = Rating.objects.filter(venue__category=category).count()
    
    context = {
        'category': category,
        'venues': venues,
        'active_venues': active_venues,
        'featured_venues': featured_venues,
        'total_ratings': total_ratings,
        'search_query': search_query,
    }
    return render(request, 'venues/admin_venues_by_category.html', context)


@login_required
def admin_edit_venues(request, category_slug):
    """Admin view for editing venues by category"""
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('venues:home')
    
    category = get_object_or_404(Category, slug=category_slug)
    venues = Venue.objects.filter(category=category).select_related('category').prefetch_related('images').order_by('-created_at')
    
    # Handle form submissions
    if request.method == 'POST':
        venue_id = request.POST.get('venue_id')
        action = request.POST.get('action')
        
        if venue_id and action == 'update':
            try:
                venue = Venue.objects.get(id=venue_id, category=category)
                venue.is_active = 'is_active' in request.POST
                venue.is_featured = 'is_featured' in request.POST
                venue.save()
                messages.success(request, f'{venue.name} updated successfully!')
            except Venue.DoesNotExist:
                messages.error(request, 'Venue not found.')
    
    context = {
        'category': category,
        'venues': venues,
    }
    return render(request, 'venues/admin_edit_venues.html', context)


@login_required
def admin_bulk_action(request, category_slug):
    """Handle bulk actions on venues"""
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('venues:home')
    
    category = get_object_or_404(Category, slug=category_slug)
    action = request.POST.get('action')
    venue_ids = request.POST.getlist('venue_ids')
    
    if not venue_ids:
        messages.error(request, 'No venues selected.')
        return redirect('venues:admin_edit_venues', category_slug=category.slug)
    
    venues = Venue.objects.filter(id__in=venue_ids, category=category)
    
    if action == 'activate':
        venues.update(is_active=True)
        messages.success(request, f'{venues.count()} venues activated successfully!')
    elif action == 'deactivate':
        venues.update(is_active=False)
        messages.success(request, f'{venues.count()} venues deactivated successfully!')
    elif action == 'delete':
        count = venues.count()
        venues.delete()
        messages.success(request, f'{count} venues deleted successfully!')
    else:
        messages.error(request, 'Invalid action.')
    
    return redirect('venues:admin_edit_venues', category_slug=category.slug)