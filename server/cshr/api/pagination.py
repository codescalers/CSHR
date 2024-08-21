from rest_framework.pagination import PageNumberPagination


class BaseGeneralUserPagination(PageNumberPagination):
    page_size = 12
    max_page_size = 50


class PendingRequestsPagination(PageNumberPagination):
    page_size = 3
    max_page_size = 10
