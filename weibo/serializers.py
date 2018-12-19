from rest_framework import serializers

from weibo.models import User, Post, Like, FollowShip, Collection
from functools import reduce


class FollowShipSerializer(serializers.ModelSerializer):
    following_user = serializers.SerializerMethodField()
    follower_user = serializers.SerializerMethodField()

    class Meta:
        model = FollowShip
        fields = ('follower', 'following', 'following_user', 'follower_user')

    def get_following_user(self, obj):
        return UserSerializer(User.objects.get(id=obj.following_id)).data

    def get_follower_user(self, obj):
        return UserSerializer(User.objects.get(id=obj.follower_id)).data


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('is_like', 'user', 'post')


class UserSerializer(serializers.ModelSerializer):
    follower_num = serializers.SerializerMethodField()
    following_num = serializers.SerializerMethodField()
    likes_earn = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'id', 'follower_num', 'following_num', 'likes_earn', 'avatar_url')

    def get_follower_num(self, obj):
        return FollowShip.objects.filter(following_id=obj.id).count()

    def get_following_num(self, obj):
        return FollowShip.objects.filter(follower_id=obj.id).count()

    def get_likes_earn(self, obj):
        if Post.objects.filter(user__id=obj.id).exists():
            queryset = Post.objects.filter(user__id=obj.id)
            return reduce(lambda x, y: x + y,
                          map(lambda x:
                              Like.objects.filter(post_id=x).filter(is_like=True).count(),
                              map(lambda x: x.id, queryset)))
        else:
            return 0

    def get_avatar_url(self, obj):
        return User.objects.get(id=obj.id).avatar.url_avatar

    def delete_fields(self, *args, **kwargs):
        fields = kwargs.get('fields')

        if fields is not None:
            forbidden = set(fields)
            existing = set(self.fields.keys())
            for field_name in forbidden:
                self.fields.pop(field_name)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)

    class Meta:
        model = Post
        fields = ('content', 'user', 'datetime')


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)
    comment = CommentSerializer(many=True)
    total_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('content', 'datetime', 'user', 'comment', 'total_liked', 'id')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def get_total_liked(self, obj):
        return Like.objects.filter(post__id=obj.id).filter(is_like=True).count()

    def delete_fields(self, *args, **kwargs):
        fields = kwargs.get('fields')

        if fields is not None:
            forbidden = set(fields)
            existing = set(self.fields.keys())
            for field_name in forbidden:
                self.fields.pop(field_name)


class CollectionSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Collection

    fields = ('posts',)

    def get_posts(self, obj):
        return PostSerializer(Post.objects.filter(id=obj.user_id)).data
