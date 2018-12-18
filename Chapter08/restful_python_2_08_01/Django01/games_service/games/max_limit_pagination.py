from rest_framework.pagination import LimitOffsetPagination


class MaxLimitPagination(LimitOffsetPagination):
    max_limit = 8
