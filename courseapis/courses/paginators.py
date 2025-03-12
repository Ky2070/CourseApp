from rest_framework import pagination

class CoursePaginatior(pagination.PageNumberPagination):
    page_size = 2