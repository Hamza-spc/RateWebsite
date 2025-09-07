# TourInsight - Venue Rating System

A Django-based web application for discovering, rating, and reviewing venues like hotels, restaurants, cafes, and more. TourInsight helps travelers make informed decisions with real reviews and ratings.

## Features

- 🏨 **Venue Discovery**: Browse venues by category and location
- ⭐ **Star Rating System**: Interactive 5-star rating with visual feedback
- 💬 **Reviews & Comments**: Write detailed reviews about your experiences
- 🔍 **Advanced Search**: Search venues by name, location, and category
- 👤 **User Authentication**: Secure login with Google OAuth integration
- 📱 **Responsive Design**: Beautiful, mobile-friendly interface
- 🛡️ **Admin Dashboard**: Manage venues, categories, and user content

## Tech Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: Django Allauth with Google OAuth
- **API**: Django REST Framework

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <your-github-repo-url>
   cd website
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp env_example.txt .env
   # Edit .env with your configuration
   ```

   **Important:** The project will work without Google OAuth setup, but you'll need to configure it for the "Sign in with Google" feature to work.

5. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data (optional)**

   ```bash
   python manage.py loaddata sample_data.json
   ```

8. **Start the development server**

   ```bash
   python manage.py runserver
   ```

9. **Visit the application**
   Open your browser and go to `http://127.0.0.1:8000`

## Optional Setup

### Video Background (Homepage)

The homepage has a video background that will fallback to a gradient if no video is found. To add a video:

1. Place your video file in `assets/videos/` as `hero-video.mp4`
2. The video should be in MP4 format and optimized for web

### Google OAuth (Optional)

The "Sign in with Google" feature requires additional setup:

1. Get Google OAuth credentials from [Google Cloud Console](https://console.cloud.google.com/)
2. Add them to your `.env` file:
   ```env
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```
3. Run: `python manage.py setup_google_oauth`

**Note:** The app works perfectly without Google OAuth - users can still sign up with email/password.

## Project Structure

```
TourInsight/
├── accounts/                 # User authentication app
├── venues/                   # Main venues app
│   ├── management/           # Custom management commands
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   ├── admin.py             # Django admin configuration
│   ├── forms.py             # Django forms
│   ├── models.py            # Database models
│   ├── urls.py              # URL patterns
│   └── views.py             # View functions
├── templates/                # Base templates
├── static/                   # Static files (CSS, JS, images)
├── assets/                   # Additional assets
├── tour_insight_system/      # Main project settings
│   ├── settings.py          # Development settings
│   ├── settings_production.py # Production settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Usage

### For Users

1. **Browse Venues**: Visit the homepage to see featured venues
2. **Search**: Use the search bar to find specific venues
3. **View Details**: Click on any venue to see detailed information
4. **Rate & Review**: Log in and click "Write a Review" to rate venues
5. **Filter by Category**: Browse venues by type (hotels, restaurants, etc.)

### For Administrators

1. **Access Admin Dashboard**: Go to `/admin-dashboard/` (requires admin privileges)
2. **Manage Venues**: Add, edit, or delete venues
3. **Manage Categories**: Organize venues by categories
4. **View Analytics**: Monitor ratings and user engagement

## API Endpoints

The application includes a REST API for programmatic access:

- `GET /api/venues/` - List all venues
- `GET /api/venues/{id}/` - Get venue details
- `POST /api/venues/` - Create new venue (admin only)
- `GET /api/ratings/` - List all ratings
- `POST /api/ratings/` - Create new rating (authenticated users)

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add your domain to authorized origins
6. Update the environment variables with your credentials

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

This project follows PEP 8 style guidelines. Use the following tools:

```bash
# Install development dependencies
pip install flake8 black

# Check code style
flake8 .

# Format code
black .
```

### Database Management

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Deployment

### Production Settings

1. Copy `venue_rating_system/settings_production.py` to your production environment
2. Set up a production database (PostgreSQL recommended)
3. Configure static file serving
4. Set up environment variables
5. Use a production WSGI server (Gunicorn recommended)

### Docker Deployment

```bash
# Build the image
docker build -t venue-rate .

# Run the container
docker run -p 8000:8000 venue-rate
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/venue-rate/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## Acknowledgments

- Django community for the excellent framework
- Tailwind CSS for the beautiful styling
- All contributors and users of this project

---

**Happy Venue Rating!** ⭐
