from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """Categories for venues (hotels, restaurants, cafes, amusement parks)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For icon class names
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Venue(models.Model):
    """Main venue model for hotels, restaurants, cafes, etc."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='venues')
    
    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Contact
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    
    # Pricing
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_range_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    
    # External booking links
    booking_com_link = models.URLField(blank=True)
    trip_com_link = models.URLField(blank=True)
    
    # Facilities and features
    facilities = models.JSONField(default=list, blank=True)  # List of facility names
    languages_spoken = models.JSONField(default=list, blank=True)  # List of languages
    amenities = models.JSONField(default=list, blank=True)  # List of amenities
    
    # Status and metadata
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Statistics (calculated fields)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_ratings = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Venue.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def update_rating_stats(self):
        """Update average rating and total counts"""
        ratings = self.ratings.all()
        if ratings.exists():
            self.average_rating = ratings.aggregate(avg=models.Avg('rating'))['avg'] or 0
            self.total_ratings = ratings.count()
            self.total_reviews = ratings.filter(comment__isnull=False).exclude(comment='').count()
        else:
            self.average_rating = 0
            self.total_ratings = 0
            self.total_reviews = 0
        self.save(update_fields=['average_rating', 'total_ratings', 'total_reviews'])


class VenueImage(models.Model):
    """Images for venues"""
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='venues/images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.venue.name} - {self.caption or 'Image'}"


class Rating(models.Model):
    """User ratings and reviews for venues"""
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['venue', 'user']  # One rating per user per venue
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.venue.name} ({self.rating}/5)"


class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profiles/avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"


class Statistics(models.Model):
    """Site statistics that get updated when venues/ratings are added"""
    total_venues = models.PositiveIntegerField(default=0)
    total_hotels = models.PositiveIntegerField(default=0)
    total_restaurants = models.PositiveIntegerField(default=0)
    total_cafes = models.PositiveIntegerField(default=0)
    total_attractions = models.PositiveIntegerField(default=0)
    total_users = models.PositiveIntegerField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    total_cities = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Statistics"
    
    def __str__(self):
        return f"Site Statistics - {self.last_updated.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def get_or_create_stats(cls):
        """Get or create the statistics object"""
        stats, created = cls.objects.get_or_create(pk=1)
        if created:
            stats.update_all_stats()
        return stats
    
    def update_all_stats(self):
        """Update all statistics"""
        from django.db.models import Count
        from django.contrib.auth.models import User
        
        # Count venues by category
        venue_counts = Venue.objects.filter(is_active=True).values('category__name').annotate(count=Count('id'))
        category_counts = {item['category__name']: item['count'] for item in venue_counts}
        
        self.total_venues = Venue.objects.filter(is_active=True).count()
        self.total_hotels = category_counts.get('Hotels', 0)
        self.total_restaurants = category_counts.get('Restaurants', 0)
        self.total_cafes = category_counts.get('Cafes', 0)
        self.total_attractions = category_counts.get('Amusement Parks', 0) + category_counts.get('Attractions', 0)
        self.total_users = User.objects.count()
        self.total_ratings = Rating.objects.count()
        self.total_cities = Venue.objects.filter(is_active=True).values('city').distinct().count()
        self.save()