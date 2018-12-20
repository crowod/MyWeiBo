from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_thumbs.fields import ImageThumbsField


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Image(models.Model):
    SIZES = (
        {'code': 'avatar', 'wxh': '125x125', 'resize': 'crop'},
        {'code': 'm', 'wxh': '640x480', 'resize': 'scale'},
        {'code': '150', 'wxh': '150x150'},  # 'resize' defaults to 'scale'
    )
    image = ImageThumbsField(upload_to='media', sizes=SIZES)


class User(AbstractUser):
    SIZES = (
        {'code': 'avatar', 'wxh': '125x125', 'resize': 'crop'},
        {'code': 'm', 'wxh': '640x480', 'resize': 'scale'},
        {'code': '150', 'wxh': '150x150'},  # 'resize' defaults to 'scale'
    )
    username = models.CharField('Username', max_length=30, unique=True)
    email = models.EmailField('Email address', unique=True)
    password = models.CharField(max_length=16)
    avatar = ImageThumbsField(upload_to='avatar', sizes=SIZES, default='avatar/default.jpg')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()


class Comment(models.Model):
    content = models.CharField(max_length=200)
    user = models.ManyToManyField(User)
    datetime = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    content = models.CharField(max_length=300, null=False)
    datetime = models.DateTimeField(auto_now_add=True)
    comment = models.ManyToManyField(Comment)
    user = models.ManyToManyField(User)


class FollowShip(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
