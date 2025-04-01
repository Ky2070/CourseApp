from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from courses.models import Category, Course, Lesson, Tag, User, Comment


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BaseSerializer(ModelSerializer):
    def to_representation(self, instance):
        d = super().to_representation(instance)
        if instance.image:
            d['image'] = instance.image.url
        return d


class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'created_at', 'category_id']


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'created_at', 'image', 'course_id']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonDetailsSerializer(LessonSerializer):
    tags = TagSerializer(many=True)
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return lesson.like_set.filter(user=request.user, activate=True).exist()

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'tags', 'liked']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save()
        return instance

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u

    def to_representation(self, instance):
        d = super().to_representation(instance)
        if instance.avatar:
            d['avatar'] = instance.avatar.url
        return d


class CommentSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(instance.user).data
        return data

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'lesson']
        extra_kwargs = {
            'lesson': {
                'write_only': True
            }
        }

