# from rest_framework.pagination import PageNumberPagination

from django.core.paginator import EmptyPage
# from django.core import paginator
from rest_framework.exceptions import ValidationError

# def paginate(queryset, request, serializer_class):

#     paginator = PageNumberPagination()
#     result_page = paginator.paginate_queryset(queryset, request)
#     serializer = serializer_class(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)





def paginate(data, paginator, page_number):
    try:
        page_number = int(page_number)
    except ValueError:
        raise ValidationError("Page number must be an integer.", code=400)

    if page_number < 1:
        raise ValidationError("Page number must be greater than 0.", code=400)

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        raise ValidationError("Page not found. Not enough data.", code=404)

    try:
        previous_page_number = page.previous_page_number()
    except EmptyPage:
        previous_page_number = None

    try:
        next_page_number = page.next_page_number()
    except EmptyPage:
        next_page_number = None

    return {
        'pagination': {
            'page': page_number,
            'page_size': len(page.object_list),
            'total_entries': paginator.count,
            'total_pages': paginator.num_pages,
            'start_index': page.start_index(),
            'end_index': page.end_index(),
            'is_previous_page': page.has_previous(),
            'previous_page_number': previous_page_number,
            'is_next_page': page.has_next(),
            'next_page_number': next_page_number,
        },
        'results': page.object_list
    }

    