from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . models import Cart,CartItem
from books.models import Book
from .serializers import CartSerializer,CartItemSerializer





class CartApiView(APIView):
    def get(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        serializer = CartSerializer(cart)
        return Response({
            "status": True,
            "message": "Cart retrieved successfully.",
            "cart": serializer.data
        })

    def post(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"status": False, "message": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        return Response({
            "status": True,
            "message": "Book added/updated in cart.",
            "item": CartItemSerializer(cart_item).data
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        book_id = request.data.get('book_id')

        try:
            cart = Cart.objects.get(user=user)
            item = CartItem.objects.get(cart=cart, book_id=book_id)
            item.delete()
            return Response({"status": True, "message": "Book removed from cart."})
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"status": False, "message": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)