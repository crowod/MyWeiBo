from django.contrib import auth
from django.shortcuts import render, redirect

# Create your views here.
from weibo.forms import LoginForm, RegisterForm
from weibo.models import User


def index_view(request):
    # if request.user.is_authenticated:
    #     return redirect('/entrance')
    # else:
    return redirect('/entrance')


def landing_view(request):
    if request.method == "POST":
        if 'username_sign_up' in request.POST:
            rf = RegisterForm(request.POST)
            if rf.is_valid():
                email = rf.cleaned_data['email_sign_up']
                username = rf.cleaned_data['username_sign_up']
                password = rf.cleaned_data['password_sign_up']
                user = User.objects.create_user(email=email, password=password, username=username)
                user.save()
            else:
                lf = LoginForm()
                return render(request, 'index.html', {'lf': lf, 'rf': rf})
        else:
            lf = LoginForm(request.POST)
            if lf.is_valid():
                email = lf.cleaned_data['email_sign_in']
                password = lf.cleaned_data['password_sign_in']
                user = auth.authenticate(username=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('/')
                else:
                    rf = RegisterForm()
                    return render(request, 'index.html',
                                  {
                                      'lf': lf,
                                      'rf': rf,
                                      'error': "password is invalid."
                                  })
            else:
                rf = RegisterForm()
                return render(request, 'index.html', {'lf': lf, 'rf': rf})

    else:
        lf = LoginForm()
        rf = RegisterForm()
        return render(request, 'index.html', {'lf': lf, 'rf': rf})
