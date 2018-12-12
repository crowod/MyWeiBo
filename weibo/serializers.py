from rest_framework import serializers

from weibo.models import User, Dynamic, Liked, FollowShip


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
        fields = ('is_liked', 'user', 'dynamic')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)

    class Meta:
        model = Dynamic
        fields = ('content', 'user', 'datetime')


class DynamicSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)
    comment = CommentSerializer(many=True)
    total_liked = serializers.SerializerMethodField()

    class Meta:
        model = Dynamic
        fields = ('content', 'datetime', 'user', 'comment', 'total_liked', 'id')

    def create(self, validated_data):
        return Dynamic.objects.create(**validated_data)

    def get_total_liked(self, obj):
        return Liked.objects.filter(dynamic__id=obj.id).filter(is_liked=True).count()
