from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator


from .models import Book
from . serializers import BookSerializer

from .utils import paginate



class BookApiView(APIView):
    def get(self, request):
        queryset = Book.objects.all().order_by('-created_at')
        page_number = request.query_params.get('page', 1)
        paginator = Paginator(queryset, 10)

        paginated_data = paginate(queryset, paginator, page_number)
        serializer = BookSerializer(paginated_data['results'], many=True)

        return Response({
            "status": True,
            "message": "Books fetched successfully.",
            "pagination": paginated_data['pagination'],
            "books": serializer.data
        })
        
        
        
    def post(self, request):
        data = request.data
        user = request.user
        vendor = user.vendor_profile
        
        if user.is_vendor:
            data['vendor'] = vendor.id
            data['category'] = data.get('category')
            serializer = BookSerializer(data=data)
            if serializer.is_valid():
                book_instance = serializer.save()
                response_serializer = BookSerializer(book_instance).data
                return Response({
                    "status" : status.HTTP_200_OK,
                    "message" : "Book added successfully",
                    "book" :response_serializer,
                },status.HTTP_201_CREATED)
                
            return Response({
                    "status" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Book adding failed",
                    "book" :serializer.errors,
                },status.HTTP_400_BAD_REQUEST)
        return Response({
                    "status" : status.HTTP_400_BAD_REQUEST
                },status.HTTP_201_CREATED)
        
        
        
    def put(self, request):
        user = request.user

        if not user.is_vendor:
            return Response({
                "status": False,
                "message": "Only vendors can update books."
            }, status=status.HTTP_403_FORBIDDEN)
            
        vendor = getattr(user, 'vendor_profile', None)
        book_id = request.data.get("id")

        if not book_id:
            return Response({
                "status": False,
                "message": "Book ID is required to update a book."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id, vendor=vendor)
        except Book.DoesNotExist:
            return Response({
                "status": False,
                "message": "Book not found or unauthorized."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Book updated successfully.",
                "book": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": "Failed to update book.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
            
