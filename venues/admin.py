from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Venue, VenueImage, Rating, UserProfile, ContactMessage, Statistics


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class VenueImageInline(admin.TabularInline):
    model = VenueImage
    extra = 1
    fields = ['image', 'caption', 'is_primary', 'order']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'city', 'country', 'average_rating', 'total_ratings', 'is_active', 'is_featured', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'city', 'country', 'created_at']
    search_fields = ['name', 'city', 'country', 'address']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [VenueImageInline]
    readonly_fields = ['average_rating', 'total_ratings', 'total_reviews', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category', 'is_active', 'is_featured')
        }),
        ('Location', {
            'fields': ('address', 'city', 'country', 'latitude', 'longitude')
        }),
        ('Contact', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Pricing', {
            'fields': ('price_range_min', 'price_range_max', 'currency')
        }),
        ('External Links', {
            'fields': ('booking_com_link', 'trip_com_link')
        }),
        ('Features', {
            'fields': ('facilities', 'languages_spoken', 'amenities')
        }),
        ('Statistics', {
            'fields': ('average_rating', 'total_ratings', 'total_reviews'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['venue', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'venue__category']
    search_fields = ['venue__name', 'user__username', 'user__email', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('venue', 'user')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_admin', 'location', 'created_at']
    list_filter = ['is_admin', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"
    
    actions = [mark_as_read]


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['total_venues', 'total_hotels', 'total_restaurants', 'total_cafes', 'total_attractions', 'total_users', 'last_updated']
    readonly_fields = ['total_venues', 'total_hotels', 'total_restaurants', 'total_cafes', 'total_attractions', 'total_users', 'total_ratings', 'total_cities', 'last_updated']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        # Update statistics when viewing the admin page
        stats = Statistics.get_or_create_stats()
        stats.update_all_stats()
        return super().changelist_view(request, extra_context)