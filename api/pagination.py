from rest_framework import pagination


class StandardResultSetPagination(pagination.PageNumberPagination):
    page_size = 100


class InterfaceResultSetPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
