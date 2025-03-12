from rest_framework.decorators import action
from rest_framework.response import Response
from courses.models import Category, Course, Lesson, User
from rest_framework import viewsets, generics, parsers
from courses import serializers, paginators
from rest_framework import status
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
    serializer_class = serializers.LessonDetailSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]