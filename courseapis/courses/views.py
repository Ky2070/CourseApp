from rest_framework.decorators import action
from rest_framework.response import Response
from courses.models import Category, Course, Lesson, User, Comment, Like
from rest_framework import viewsets, generics, parsers, permissions, status
from courses import serializers, paginators, perms


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(activate=True)
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(activate=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.CoursePaginatior

    def get_queryset(self):
        query = self.queryset
        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                query = query.filter(subject__icontains=q)

            cate_id = self.request.query_params.get('category_id')
            if cate_id:
                query = query.filter(category_id=cate_id)

        return query

    @action(methods=['get'], url_path='lesson', detail=True)
    def get_lesson(self, request, pk):
        lessons = self.get_object().lesson_set.filter(activate=True)

        q = self.request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)

        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(activate=True)
    serializer_class = serializers.LessonDetailsSerializer

    def get_permissions(self):
        if self.action.__eq__('get_comment'):
            if self.request.method.__eq__('POST'):
                return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'post'], url_path='comments', detail=True)
    def get_comment(self, request, pk):
        if request.method.__eq__('POST'):
            t = serializers.CommentSerializer(data={
                'content': request.data.get('content'),
                'user': request.user.pk,
                'lesson': pk
            })
            t.is_valid(raise_exception=True)
            c = t.save()
            return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        else:
            comments = self.get_object().comment_set.select_related('user').filter(activate=True)
            p = paginators.CommentPaginator()
            page = p.paginate_queryset(comments, self.request)
            if page is not None:
                serializer = serializers.CommentSerializer(page, many=True)
                return p.get_paginated_response(serializer.data)
            else:
                return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        li, created = Like.objects.get_or_create(user=request.user, lesson=self.get_object())
        if not created:
            li.active = not li.active

        li.save()
        return Response(serializers.LessonDetailsSerializer(self.get_object(), context={'request': self.request}).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.filter(activate=True)
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.OwnerComment]


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [perms.OwnerPerms()]

        return [permissions.AllowAny]

    @action(methods=['get'], url_path='current-user', detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)
