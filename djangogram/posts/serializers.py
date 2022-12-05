#필요한 데이터를 명시
from rest_framework import serializers
from djangogram.users.models import User as user_model
from . import models

# 모델명시, 필요한 필드
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = (
            "id",
            "contents"
        )


class FeedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = (
            "id",
            "username",
            "profile_photo"
        )

class PostSerializer(serializers.ModelSerializer):
    comment_post = CommentSerializer(many=True)
    author = FeedAuthorSerializer()

    class Meta:
        model = models.Post
        fields = (
            "id",
            "image",
            "caption",  
            "comment_post", # post를 외래키로 가지는 놈 보면 됨
            "author",
        )
    