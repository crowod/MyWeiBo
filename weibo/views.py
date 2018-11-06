from django.contrib import auth
from django.shortcuts import render, redirect

# Create your views here.
from weibo.forms import LoginForm, RegisterForm, ProfileForm
from weibo.models import User

current_url = ""


def index_view(request):
    global current_url
    if request.user.is_authenticated:
        current_url = '/profile'
        return redirect('/profile')
    else:
        return redirect('/entrance')


def landing_view(request):
    global current_url
    current_url = '/entrance'
    if request.method == "POST":
        if 'username_sign_up' in request.POST:
            rf = RegisterForm(request.POST)
            if rf.is_valid():
                email = rf.cleaned_data['email_sign_up']
                username = rf.cleaned_data['username_sign_up']
                password = rf.cleaned_data['password_sign_up']
                user = User.objects.create_user(email=email, password=password, username=username)
                user.save()
                return redirect('/')
            else:
                lf = LoginForm()
                return render(request, 'entrance.html', {'lf': lf, 'rf': rf, 'status': 1})
        else:
            lf = LoginForm(request.POST)
            if lf.is_valid():
                email = lf.cleaned_data['email_sign_in']
                password = lf.cleaned_data['password_sign_in']
                user = auth.authenticate(username=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('/profile')
                else:
                    rf = RegisterForm()
                    return render(request, 'entrance.html',
                                  {
                                      'lf': lf,
                                      'rf': rf,
                                      'error': "password is invalid."
                                  })
            else:
                rf = RegisterForm()
                return render(request, 'entrance.html', {'lf': lf, 'rf': rf, 'status': 0})

    else:
        lf = LoginForm()
        rf = RegisterForm()
        return render(request, 'entrance.html', {'lf': lf, 'rf': rf})


def profile_view(request):
    global current_url
    current_url = '/profile'
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        if request.method == "POST":
            profile_form = ProfileForm(request.POST)
            if profile_form.is_valid():
                email = profile_form.cleaned_data['email_profile']
                password = profile_form.cleaned_data['password_profile_new']
                # username here do not be loaded, modify this
                username = user.username
                User.objects.filter(username=username).update(email=email, password=password)
                return render(request, "profile.html", {"profile_form": profile_form,
                                                        "success_msg": "Update successfully!",
                                                        "username": username})
            else:
                return render(request, "profile.html", {"error": profile_form.errors,
                                                        "profile_form": profile_form,
                                                        "username": ""})
        else:
            profile_form = ProfileForm()
            # username here do not be loaded, modify this
            username = user.username
            return render(request, "profile.html", {"profile_form": profile_form,
                                                    "username": username})
    else:
        return redirect('/entrance')


def logout_view(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/entrance')
    else:
        return redirect(current_url)
