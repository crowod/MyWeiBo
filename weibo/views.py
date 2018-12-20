from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
# Create your views here.
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from weibo.forms import LoginForm, RegisterForm, ProfileForm
from weibo.models import User, Post, Like, FollowShip, Comment
from weibo.serializers import PostSerializer, LikeSerializer, UserSerializer, FollowShipSerializer, \
    CommentSerializer

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


def otherPost_view(request, username):
    if request.user.is_authenticated:
        if request.user.username == username:
            return redirect('/post')
        return render(request, 'othersPost.html', {'username': username})
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


def otherFollower_view(request, username):
    if request.user.is_authenticated:
        return render(request, 'otherFollower.html', {'username': username})
    else:
        return render(request, 'home.html')


def otherFollowing_view(request, username):
    if request.user.is_authenticated:
        return render(request, 'otherFollow.html', {'username': username})
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
                                      'error': "password is invalid.",
                                      'status': status
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
            profile_form = ProfileForm(request.POST)
            if profile_form.is_valid():
                password = profile_form.cleaned_data['password_profile_new']
                username = user.username
                user = User.objects.get(username=username)
                password_old = profile_form.cleaned_data['password_profile_old']
                if user.check_password(password_old) is False:
                    profile_form.add_error('password_profile_old', 'invalid old password')
                    username = user.username
                    user = User.objects.get(username=username)
                    return render(request, "profile.html", {"profile_form": profile_form,
                                                            "user": user,
                                                            "status": 1})
                else:
                    user.set_password(password)
                    update_session_auth_hash(request, user)
                    user.save()
                return render(request, "profile.html", {"profile_form": profile_form,
                                                        "success_msg": "Update successfully!",
                                                        "user": user,
                                                        "status": 0})
            else:
                return render(request, "profile.html", {"error": profile_form.errors,
                                                        "profile_form": profile_form,
                                                        "user": user,
                                                        "status": 1})
        else:
            profile_form = ProfileForm()
            username = user.username
            user = User.objects.get(username=username)
            return render(request, "profile.html", {"profile_form": profile_form,
                                                    "user": user,
                                                    "status": 0})
    else:
        return redirect('/entrance')


def logout_view(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')
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
        serializer.delete_fields(fields=['id'])
        queryset = Post.objects.filter(user__username=username)
        post_id = list(map(lambda x: x.id, queryset))
        result = {'post_id': post_id}
        result.update(serializer.data)
        queryset = Like.objects.filter(user__username=username).filter(is_like=True)
        like_post_id = list(map(lambda x: x.post_id, queryset))
        result.update({'like_post_id': like_post_id})
        return Response({
            'data': result
        }, status=status.HTTP_200_OK)


class UserProfile(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        queryset = User.objects.get(username=username)
        serializer = UserSerializer(queryset)
        serializer.delete_fields(fields=['id'])
        if request.user.username:
            is_following = FollowShip.objects.filter(follower__username=request.user.username,
                                                     following__username=kwargs['username']).exists()
            queryset = Like.objects.filter(user__username=request.user.username).filter(is_like=True)
            like_post_id = list(map(lambda x: x.post_id, queryset))
            result = dict()
            result.update(serializer.data)
            result.update({'like_post_id': like_post_id})
            return Response({
                'data': result,
                'is_following': is_following
            }, status=status.HTTP_200_OK)
        return Response({
            'data': serializer.data,
        }, status=status.HTTP_200_OK)


class PostUser(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'user'

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(user__username=kwargs['name']).order_by('-datetime')
        serializer = PostSerializer(queryset, many=True)
        serializer_list = list(serializer.data)
        [x.pop('user') for x in serializer_list]
        if serializer:
            return Response({
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class PostAdd(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        content = request.data['content']
        if content.strip() == '':
            return Response(status=status.HTTP_404_NOT_FOUND)
        datetime = timezone.now()
        user = User.objects.get(username=request.user.username)
        post = Post.objects.create(content=content, datetime=datetime)
        post.user.add(user)
        queryset = Post.objects.all().order_by('-datetime')
        serializer = PostSerializer(queryset, many=True)
        queryset = Post.objects.filter(user__username=request.user.username)
        posts_id = list(map(lambda x: x.id, queryset))
        return Response({
            'data': serializer.data,
            'posts_id': posts_id
        }, status=status.HTTP_201_CREATED, )


class PostDelete(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        post_id = request.data['post_id']
        username = request.user.username
        user = User.objects.get(username=username)
        Post.objects.get(user=user, id=post_id).delete()
        return Response(status=status.HTTP_201_CREATED)


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all().order_by('-datetime')
        serializer = PostSerializer(queryset, many=True)
        if serializer:
            return Response({
                'data': serializer.data
            }, status=status.HTTP_200_OK, )
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class PostLike(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        username = request.user.username
        post_id = request.data['post_id']
        user = User.objects.get(username=username)
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=user, post=post, defaults={'is_like': False})
        if like.is_like is True:
            like.is_like = False
        else:
            like.is_like = True
        like.save()
        total_like = Like.objects.filter(post=post).filter(is_like=True).count()
        if like:
            return Response({
                'total_like': total_like
            }, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class FollowerList(generics.ListAPIView):
    queryset = FollowShip.objects.all()
    serializer_class = FollowShipSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        queryset = FollowShip.objects.filter(following__username=username)
        serializer = FollowShipSerializer(queryset, many=True)
        result = [x.get('follower_user') for x in serializer.data]
        if request.user.username:
            for item in result:
                is_following = FollowShip.objects.filter(follower__username=request.user.username,
                                                         following__username=item.get('username')).exists()
                item.update({'is_following': is_following})
            return Response({
                'data': result
            }, status=status.HTTP_200_OK)
        if serializer:
            return Response({
                'data': result
            }, status=status.HTTP_200_OK, )
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class FollowingList(generics.ListAPIView):
    queryset = FollowShip.objects.all()
    serializer_class = FollowShipSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        queryset = FollowShip.objects.filter(follower__username=username)
        serializer = FollowShipSerializer(queryset, many=True)
        result = [x.get('following_user') for x in serializer.data]
        if request.user.username:
            for item in result:
                is_following = FollowShip.objects.filter(follower__username=request.user.username,
                                                         following__username=item.get('username')).exists()
                item.update({'is_following': is_following})
            return Response({
                'data': result
            }, status=status.HTTP_200_OK)
        if serializer:
            return Response({
                'data': result
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class FollowingAdd(generics.CreateAPIView):
    queryset = FollowShip.objects.all()
    serializer_class = FollowShipSerializer

    def post(self, request, *args, **kwargs):
        username = request.user.username
        following_name = request.data['following_name']
        user = User.objects.get(username=username)
        following = User.objects.get(username=following_name)
        follow_ship = FollowShip.objects.create(follower=user, following=following)
        if follow_ship:
            return Response(
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class FollowingCancel(generics.CreateAPIView):
    queryset = FollowShip.objects.all()
    serializer_class = FollowShipSerializer

    def post(self, request, *args, **kwargs):
        username = request.user.username
        following_name = request.data['following_name']
        user = User.objects.get(username=username)
        following = User.objects.get(username=following_name)
        FollowShip.objects.filter(follower=user, following=following).delete()
        return Response(
            status=status.HTTP_201_CREATED
        )


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
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class CommentAdd(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        username = request.user.username
        post_id = request.data['post_id']
        content = request.data['content']
        datetime = timezone.now()
        user = User.objects.get(username=username)
        comment = Comment.objects.create(content=content, datetime=datetime)
        comment.user.add(user)
        Post.objects.get(id=post_id).comment.add(comment)
        return Response(
            status=status.HTTP_201_CREATED
        )


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

                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({

                'data': serializer.data
            }, status=status.HTTP_404_NOT_FOUND)


class PostSearch(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        keyword = request.data['keyword']
        queryset = Post.objects.filter(content__icontains=keyword)
        serializer = PostSerializer(queryset, many=True)
        if serializer:
            return Response({
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'data': serializer.data
            }, status=status.HTTP_404_NOT_FOUND)


class RecommendationList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.exclude(username=request.user.username)
        serializer = UserSerializer(queryset, many=True)
        serializer.delete_fields(fields=['id', 'following_num', 'likes_earn'])
        result = sorted(serializer.data, key=lambda x: x.get('follower_num'))
        return Response({
            'data': result
        }, status=status.HTTP_200_OK)


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
        image = request.FILES['file']
        username = request.user.username
        user = User.objects.get(username=username)
        user.avatar = image
        user.save()
        if user:
            return Response({
                'avatar_url': user.avatar.url_avatar
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
