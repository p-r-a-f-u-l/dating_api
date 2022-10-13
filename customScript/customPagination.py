from rest_framework import pagination


class CustomZeroPagination(pagination.PageNumberPagination):
    page_size = 0
