from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from venues.models import UserProfile, Rating
from .forms import UserProfileForm


@login_required
def profile(request):
    """User profile page"""
    user_ratings = Rating.objects.filter(user=request.user).select_related('venue').order_by('-created_at')
    
    context = {
        'user_ratings': user_ratings,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/edit_profile.html', context)