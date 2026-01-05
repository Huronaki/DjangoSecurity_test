from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from .forms import RegisterForm, ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
import csv
import re
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User


#  Against CSV Injection
def strict_safe_csv(value):
    if not value:
        return value

    # deny by default
    value = re.sub(r'[^\w\s.,!?-_]', '', value)

    # Security for CSV Injection
    if value and value[0] in ('=', '+', '-', '@'):
        value = "'" + value

    return value


def index(request):
    return HttpResponse("My first django-site")


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html', {'profile': request.user.profile})


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def export_profile_csv(request):
    user_id = request.GET.get('user_id')

    try:
        if user_id:
            user = User.objects.get(id=user_id)
        else:
            user = request.user
        profile = user.profile
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)
    except Profile.DoesNotExist:
        return HttpResponse("Profile not found", status=404)
    

    user = request.user
    profile = user.profile

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="profile.csv"'

    writer = csv.writer(response)
    writer.writerow(['username', 'bio', 'avatar'])
    writer.writerow([
        user.username,
        profile.bio,
        profile.avatar.url if profile.avatar else ''
    ])

    return response

