from rest_framework import serializers

from weibo.models import User, Post, Liked, FollowShip, Collection


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


class LikedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liked
        fields = ('is_liked', 'user', 'post')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


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
        return Liked.objects.filter(post__id=obj.id).filter(is_liked=True).count()


class CollectionSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Collection

    fields = ('posts',)

    def get_posts(self, obj):
        return PostSerializer(Post.objects.filter(id=obj.user_id)).data
