import json
import re

from django.contrib import auth
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
# Create your views here.
from django.utils import timezone
from django.core.validators import validate_email
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from weibo.forms import LoginForm, RegisterForm, ProfileForm
from weibo.models import User, Post, Liked, FollowShip, Comment
from weibo.serializers import PostSerializer, LikedSerializer, UserSerializer, FollowShipSerializer, \
    CommentSerializer
from . import forms

current_url = ""


def index_view(request):
    global current_url
    if request.user.is_authenticated:
        current_url = '/'
        return render(request, "index.html")

    else:
        return render(request, 'home.html')


def post_view(request):
    if request.user.is_authenticated:
        return render(request, 'userPost.html')
    else:
        return render(request, 'home.html')


def following_view(request):
    if request.user.is_authenticated:
        return render(request, 'userFollow.html')
    else:
        return render(request, 'home.html')


def follower_view(request):
    if request.user.is_authenticated:
        return render(request, 'userFollower.html')
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
                try:
                    validate_email(email)
                    user = auth.authenticate(email=email, password=password)
                except ValidationError:
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
            user = User.objects.get(username=username)
            return render(request, "profile.html", {"profile_form": profile_form,
                                                    "user": user})
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


class MyProfile(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        username = request.user.username
        queryset = User.objects.get(username=username)
        serializer = UserSerializer(queryset)
        queryset = FollowShip.objects.filter(following__username=username)
        serializer_follower = FollowShipSerializer(queryset, many=True)
        follower_num = len([x.get('follower_user') for x in serializer_follower.data])
        queryset = FollowShip.objects.filter(follower__username=username)
        serializer_following = FollowShipSerializer(queryset, many=True)
        following_num = len([x.get('following_user') for x in serializer_following.data])
        new_dict = {'following_num': following_num,
                    'follower_num': follower_num}
        new_dict.update(serializer.data)
        new_dict.pop('id')
        return Response({
            'status': status.HTTP_200_OK,
            'data': new_dict
        })


class PostUser(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'user'

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(user__username=kwargs['name']).order_by('-datetime')
        serializer = PostSerializer(queryset, many=True)
        queryset_liked = Liked.objects.filter(user__username=kwargs['name'])
        serializer_liked = LikedSerializer(queryset_liked, many=True)
        serializer_list = list(serializer.data)
        serializer_liked_list = list(serializer_liked.data)
        [y.update({'is_liked': z.get('is_liked')}) for x in serializer_list for y in x.get('user') for z in
         serializer_liked_list if z.get('user') == y.get('id') and z.get('post') == x.get('id')]
        if serializer:
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class PostAdd(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        content = request.data['content']
        datetime = timezone.now()
        user = User.objects.get(username=request.user.username)
        post = Post.objects.create(content=content, datetime=datetime)
        post.user.add(user)
        Liked.objects.create(user=user, post=post)
        return Response({
            'status': status.HTTP_201_CREATED
        })


class PostDelete(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        post_id = request.data['post_id']
        username = request.data['username']
        user = User.objects.get(username=username)
        Liked.objects.get(user=user, post_id=post_id).delete()
        Post.objects.get(user=user, id=post_id).delete()
        return Response({
            'status': status.HTTP_201_CREATED
        })


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all().order_by('-datetime')
        serializer = PostSerializer(queryset, many=True)
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
    queryset = Liked.objects.all()
    serializer_class = LikedSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        post_id = request.data['post_id']
        is_liked = request.data['is_liked']
        user = User.objects.get(username=username)
        post = Post.objects.get(id=post_id)
        liked = Liked.objects.update_or_create(user=user, post=post, defaults={"is_liked": is_liked})
        if liked:
            return Response({
                'status': status.HTTP_201_CREATED
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class FollowerList(generics.ListAPIView):
    queryset = FollowShip.objects.all()
    serializer_class = FollowShipSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        queryset = FollowShip.objects.filter(following__username=username)
        serializer = FollowShipSerializer(queryset, many=True)
        result = [x.get('follower_user') for x in serializer.data]
        if serializer:
            return Response({
                'status': status.HTTP_200_OK,
                'data': result
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class FollowingList(generics.ListAPIView):
    queryset = FollowShip.objects.all()
    serializer_class = FollowShipSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        queryset = FollowShip.objects.filter(follower__username=username)
        serializer = FollowShipSerializer(queryset, many=True)
        result = [x.get('following_user') for x in serializer.data]
        if serializer:
            return Response({
                'status': status.HTTP_200_OK,
                'data': result
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class FollowingAdd(generics.CreateAPIView):
    queryset = FollowShip.objects.all()
    serializer_class = FollowShipSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        following_name = request.data['following_name']
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
    queryset = FollowShip.objects.all()
    serializer_class = FollowShipSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        following_name = request.data['following_name']
        user = User.objects.get(username=username)
        following = User.objects.get(username=following_name)
        FollowShip.objects.get(follower=user, following=following).delete()
        return Response({
            'status': status.HTTP_201_CREATED
        })


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        post_id = request.data['post_id']
        post = Post.objects.get(id=post_id)
        queryset = Comment.objects.filter(post=post)
        serializer = CommentSerializer(queryset, many=True)
        if serializer:
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND
            })


class CommentAdd(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        post_id = request.data['post_id']
        content = request.data['content']
        datetime = timezone.now()
        user = User.objects.get(username=username)
        comment = Comment.objects.create(content=content, datetime=datetime)
        comment.user.add(user)
        Post.objects.get(id=post_id).comment.add(comment)
        return Response({
            'status': status.HTTP_201_CREATED
        })


class CommentDelete(generics.CreateAPIView):
    pass


class UserSearch(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        keyword = request.data['keyword']
        queryset = User.objects.filter(username__icontains=keyword)
        serializer = UserSerializer(queryset, many=True)
        if serializer:
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'data': serializer.data
            })


class PostSearch(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        keyword = request.data['keyword']
        queryset = Post.objects.filter(content__icontains=keyword)
        serializer = PostSerializer(queryset, many=True)
        if serializer:
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })
        else:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'data': serializer.data
            })


class CollectionList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        pass


class CollectionAdd(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        pass


class CollectionCancel(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        pass


class AvatarUpload(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        pass
