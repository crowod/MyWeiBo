from django.shortcuts import render, redirect
from .forms import ProfileForm


def profile_view(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            email = profile_form.cleaned_data['email_profile']
            password = profile_form.cleaned_data['password_profile_new']
            return render(request, "profile.html", {"profile_form": profile_form, "success_msg": "Update successfully!"})
        else:
            return render(request, "profile.html", {"error": profile_form.errors, "profile_form": profile_form})
    else:
        profile_form = ProfileForm()
        return render(request, "profile.html", {"profile_form": profile_form, "username": "123name"})

