from rest_framework import pagination


class CoursePaginatior(pagination.PageNumberPagination):
    page_size = 6


class CommentPaginator(pagination.PageNumberPagination):
    page_size = 3
