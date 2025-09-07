from django.core.management.base import BaseCommand
from django.utils.text import slugify
from venues.models import Venue

class Command(BaseCommand):
    help = 'Fix venues with empty or missing slugs'

    def handle(self, *args, **options):
        venues_without_slugs = Venue.objects.filter(slug__isnull=True) | Venue.objects.filter(slug='')
        
        if not venues_without_slugs.exists():
            self.stdout.write(self.style.SUCCESS('No venues with empty slugs found.'))
            return
        
        self.stdout.write(f'Found {venues_without_slugs.count()} venues with empty slugs. Fixing...')
        
        fixed_count = 0
        for venue in venues_without_slugs:
            original_slug = slugify(venue.name)
            venue.slug = original_slug
            
            # Ensure uniqueness
            counter = 1
            while Venue.objects.filter(slug=venue.slug).exclude(pk=venue.pk).exists():
                venue.slug = f"{original_slug}-{counter}"
                counter += 1
            
            venue.save()
            fixed_count += 1
            self.stdout.write(f'Fixed: {venue.name} -> {venue.slug}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {fixed_count} venue slugs.')
        )
