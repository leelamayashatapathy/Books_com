from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . models import Cart,CartItem,Order,OrderItem,VendorOrder,OrderStatus
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
        
        
        
class OrderApiView(APIView):
    def post(self,request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"status": False, "message": "Cart not found."}, status=404)

        cart_items = cart.items.all().values()
        if not cart_items.exists():
            return Response({"status": False, "message": "Cart is empty."}, status=400)
        
        shipping_address = user.addresses.filter(is_default=True).first()
        if not shipping_address:
            return Response({"status": False, "message": "No default address found."}, status=400)

        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            total_amount=0
        )

        total = 0
        vendor_map = {}

        for item in cart_items:
            print(item)

            try:
                book = Book.objects.get(id=item.get('book_id'))
            except Book.DoesNotExist:
                continue  

            vendor = book.vendor.user
            quantity = item.get('quantity')
            order_item = OrderItem.objects.create(
                order=order,
                book=book,
                quantity=quantity,
                price=book.price
            )
            total += quantity * book.price

            if vendor not in vendor_map:
                vendor_map[vendor] = []
            vendor_map[vendor].append(order_item)

        order.total_amount = total
        order.save()

        for vendor, items in vendor_map.items():
            VendorOrder.objects.create(
                order=order,
                vendor=vendor,
                status=OrderStatus.PENDING,
                bok_order_id=f"{order.id}-{vendor.id}"
            )

        cart.items.all().delete()

        return Response({
            "status": True,
            "message": "Order placed successfully.",
            "order_id": order.id,
            "total": float(total),
        }, status=201)