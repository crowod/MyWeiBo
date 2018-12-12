from django.contrib import auth
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from rest_framework.response import Response

from weibo.forms import LoginForm, RegisterForm, ProfileForm
from weibo.models import User, Dynamic, Liked, FollowShip
from weibo.serializers import DynamicSerializer, LikedSerializer, UserSerializer, FollowShipSerializer
from . import forms
from rest_framework import generics, status

current_url = ""


def index_view(request):
    global current_url
    if request.user.is_authenticated:
        current_url = '/'
        return render(request, "feed.html")

    else:
        return render(request, 'home.html')


def landing_view(request, status=0):
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
                    return redirect('/')
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
        return render(request, 'entrance.html', {'lf': lf, 'rf': rf, 'status': status})


def profile_view(request):
    global current_url
    current_url = '/profile'
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        if request.method == "POST":
            forms.user = user
            profile_form = ProfileForm(request.POST)
            if profile_form.is_valid():
                email = profile_form.cleaned_data['email_profile']
                password = profile_form.cleaned_data['password_profile_new']
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


def sign_in(request):
    return landing_view(request, status=0)


def sign_up(request):
    return landing_view(request, status=1)


class DynamicUser(generics.ListAPIView):
    queryset = Dynamic.objects.all()
    serializer_class = DynamicSerializer
    lookup_field = 'user'

    def get(self, request, *args, **kwargs):
        queryset = Dynamic.objects.filter(user__username=kwargs['name']).order_by('datetime')
        serializer = DynamicSerializer(queryset, many=True)
        queryset_liked = Liked.objects.filter(user__username=kwargs['name'])
        serializer_liked = LikedSerializer(queryset_liked, many=True)
        serializer_list = list(serializer.data)
        serializer_liked_list = list(serializer_liked.data)
        result = [y.update({'is_liked': z.get('is_liked')}) for x in serializer_list for y in x.get('user') for z in
                  serializer_liked_list if z.get('user') == y.get('id') and z.get('dynamic') == x.get('id')]
        if serializer:
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class DynamicAdd(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        content = request.query_params['content']
        datetime = timezone.now()
        user = User.objects.get(username=kwargs['name'])
        result = Dynamic.objects.create(content=content, datetime=datetime).user.add(user)
        if result:
            return Response({
                'status': status.HTTP_201_CREATED
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class DynamicDelete(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        dynamic_id = request.query_params['dynamic_id']
        user = User.objects.get(username=kwargs['name'])
        result = Dynamic.objects.get(user=user, dynamic_id=dynamic_id).delete()
        if result:
            return Response({
                'status': status.HTTP_201_CREATED
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class DynamicList(generics.ListAPIView):
    queryset = Dynamic.objects.all()
    serializer_class = DynamicSerializer

    def get(self, request, *args, **kwargs):
        queryset = Dynamic.objects.all().order_by('datetime')
        serializer = DynamicSerializer(queryset, many=True)
        if serializer:
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class PostLiked(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        username = request.query_params['username']
        dynamic_id = request.query_params['dynamic_id']
        is_liked = request.query_params['is_liked']
        user = User.objects.get(username=username)
        dynamic = Dynamic.objects.get(id=dynamic_id)
        liked = Liked.objects.update_or_create(user=user, dynamic=dynamic, defaults={"is_liked": is_liked})
        if liked:
            return Response({
                'status': status.HTTP_201_CREATED
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class FollowerList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        queryset = FollowShip.objects.filter(follower__username=username)
        serializer = FollowShipSerializer(queryset, many=True)
        if serializer:
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class FollowingList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        queryset = FollowShip.objects.filter(following__username=username)
        serializer = FollowShipSerializer(queryset, many=True)
        if serializer:
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class FollowingAdd(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        username = request.query_params['username']
        following_name = request.query_params['following_name']
        user = User.objects.get(username=username)
        following = User.objects.get(username=following_name)
        follow_ship = FollowShip.objects.create(follower=user, following=following)
        if follow_ship:
            return Response({
                'status': status.HTTP_201_CREATED
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class FollowingCancel(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        username = request.query_params['username']
        following_name = request.query_params['following_name']
        user = User.objects.get(username=username)
        following = User.objects.get(username=following_name)
        follow_ship = FollowShip.objects.get(follower=user, following=following).delete()
        if follow_ship:
            return Response({
                'status': status.HTTP_201_CREATED
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class CommentList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        dynamic_id = request.query_params['dynamic_id']
        dynamic = Dynamic.objects.get(id=dynamic_id)


class PostComment(generics.CreateAPIView):
    pass
