from django.core.management.base import BaseCommand
from django.core.files import File
from venues.models import Venue, VenueImage
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Add sample images to venues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--venue-slug',
            type=str,
            help='Slug of the venue to add images to',
        )
        parser.add_argument(
            '--image-path',
            type=str,
            help='Path to the image file',
        )

    def handle(self, *args, **options):
        venue_slug = options['venue_slug']
        image_path = options['image_path']
        
        if not venue_slug or not image_path:
            self.stdout.write(
                self.style.ERROR('Please provide both --venue-slug and --image-path')
            )
            return
        
        try:
            venue = Venue.objects.get(slug=venue_slug)
        except Venue.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Venue with slug "{venue_slug}" not found')
            )
            return
        
        if not os.path.exists(image_path):
            self.stdout.write(
                self.style.ERROR(f'Image file "{image_path}" not found')
            )
            return
        
        # Create venue image
        with open(image_path, 'rb') as f:
            venue_image = VenueImage.objects.create(
                venue=venue,
                image=File(f),
                caption=f"Image for {venue.name}",
                is_primary=not venue.images.exists(),  # Make first image primary
                order=venue.images.count()
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added image to {venue.name}')
        )
