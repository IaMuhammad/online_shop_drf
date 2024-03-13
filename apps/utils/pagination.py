from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Custom query parameter for page size
    max_page_size = 100  # Maximum allowed value for page size

    def get_page_size(self, request):
        """
        Get the custom page size from the request query parameters.
        """
        page_size = request.query_params.get(self.page_size_query_param)
        if page_size:
            try:
                return int(page_size)
            except ValueError:
                pass
        return self.page_size

    def get_paginated_response(self, data):
        """
        Return a custom paginated response with metadata.
        """
        return Response({
            'count': self.page.paginator.count,
            'page_size': self.page.paginator.per_page,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

    def paginate_queryset(self, queryset, request, view=None):

        return super().paginate_queryset(queryset, request, view=view)
