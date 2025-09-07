# ✅ Quick Setup Checklist

Use this checklist to ensure your friend doesn't miss anything when setting up the project.

## 🚀 Essential Setup (Must Do)

- [ ] **Navigate to Desktop**: 
  - Windows: `cd %USERPROFILE%\Desktop`
  - macOS/Linux: `cd ~/Desktop`
- [ ] **Clone repository**: `git clone https://github.com/Hamza-spc/RateWebsite.git`
- [ ] **Navigate to project**: `cd RateWebsite`
- [ ] **Create virtual environment**: `python -m venv venv`
- [ ] **Activate virtual environment**: 
  - Windows: `venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
- [ ] **Install dependencies**: `pip install -r requirements.txt`
- [ ] **Copy environment file**: `cp env_example.txt .env`
- [ ] **Run migrations**: `python manage.py migrate`
- [ ] **Create superuser**: `python manage.py createsuperuser`
- [ ] **Start server**: `python manage.py runserver`
- [ ] **Test homepage**: Visit http://127.0.0.1:8000

## 🎯 Optional Setup (Nice to Have)

- [ ] **Add sample data**: Use the Python shell commands in DEVELOPER_SETUP.md
- [ ] **Configure Google OAuth**: Add credentials to .env file
- [ ] **Add video background**: Place hero-video.mp4 in assets/videos/
- [ ] **Customize .env**: Set your preferred settings

## 🧪 Testing Checklist

- [ ] **Homepage loads**: No errors, beautiful design
- [ ] **Search works**: Try searching for "hotel" or "restaurant"
- [ ] **Venue details**: Click on any venue to see details
- [ ] **User registration**: Go to /accounts/signup/
- [ ] **User login**: Go to /accounts/login/
- [ ] **Star rating**: Login and try rating a venue
- [ ] **Admin panel**: Go to /admin/ with superuser account
- [ ] **Admin dashboard**: Go to /admin-dashboard/

## 🐛 Common Issues & Solutions

- [ ] **Port 8000 busy**: Use `python manage.py runserver 8001`
- [ ] **Import errors**: Make sure virtual environment is activated
- [ ] **Database errors**: Run `python manage.py migrate`
- [ ] **Permission errors**: Check file permissions
- [ ] **Static files not loading**: Run `python manage.py collectstatic`

## 📱 What Should Work After Setup

- [ ] **Responsive design**: Test on mobile/tablet
- [ ] **Star rating system**: Click stars to rate venues
- [ ] **User authentication**: Sign up, login, logout
- [ ] **Venue management**: Add/edit venues via admin
- [ ] **Search functionality**: Find venues by name/location
- [ ] **Review system**: Write and view reviews

## 🎉 Success Indicators

If everything is working correctly, you should see:

- ✅ Homepage loads with beautiful design
- ✅ Can browse and search venues
- ✅ Can create user accounts
- ✅ Can rate venues with stars
- ✅ Admin panel accessible
- ✅ No error messages in browser console
- ✅ Fast page loading times

---

**Total setup time: ~10-15 minutes** ⏱️

**Need help?** Check DEVELOPER_SETUP.md for detailed instructions!
