from rest_framework import serializers

from .models import User, Material, Comment, Mark


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]


class MaterialBaseSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    total_score = serializers.SerializerMethodField(read_only=True)
    total_voices = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Material
        fields = [
            'id',
            'author',
            'material_type',
            'title',
            'published',
            'total_score',
            'total_voices'
        ]

    def get_total_score(self, obj):
        return obj.pluses - obj.minuses

    def get_total_voices(self, obj):
        return obj.pluses + obj.minuses


class MarkBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = [
            'id',
            'mark'
        ]


class MarkSerializer(MarkBaseSerializer):
    author = AuthorSerializer()

    class Meta(MarkBaseSerializer.Meta):
        fields = MarkBaseSerializer.Meta.fields + [
            'author',
            'added',
            'updated'
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'added',
            'updated',
            'text'
        ]


class MaterialSerializer(MaterialBaseSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(MaterialBaseSerializer.Meta):
        fields = MaterialBaseSerializer.Meta.fields + [
            'text',
            'added',
            'updated',
            'pluses',
            'minuses',
            'comments',
        ]
