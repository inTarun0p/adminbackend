import os
from django.shortcuts import render,redirect
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .Serializer import ProductSerializer

# Create your views here.
@api_view(['POST'])
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        productid = request.POST.get('productid')
        category = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        sales = request.POST.get('sales')
        image = request.FILES.get('image')

        product = Product(name=name, productid=productid, category=category, price=price, stock=stock, sales=sales, image=image)
        product.save()

        return  Response({'message': 'Product added successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        count = Product.objects.count()
        serializer = ProductSerializer(products, many=True)
        return Response({'count': count, 'data': serializer.data})
    return Response(
        {'error': 'Invalid request method'},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
def delete_products(request):
    if request.method == "POST":
        print("Delete request received. Data:", request.data)  # Debug log
        try:
            # Try to get ID from both form data and JSON
            product_id = request.data.get('id') or request.POST.get('id')
            print("Raw product ID:", product_id)  # Debug log
            
            if not product_id:
                print("No product ID provided")  # Debug log
                return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                product_id = int(product_id)  # Ensure ID is an integer
                print("Parsed product ID:", product_id)  # Debug log
            except (ValueError, TypeError) as e:
                print(f"Error parsing product ID: {e}")  # Debug log
                return Response({'error': 'Invalid product ID'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                product = Product.objects.get(id=product_id)
                print("Found product:", product)  # Debug log
            except Product.DoesNotExist:
                print(f"Product with ID {product_id} not found")  # Debug log
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Store the image path before deleting
            image_path = product.image.path if product.image else None
            print("Image path:", image_path)  # Debug log
            
            # Delete the product
            product.delete()
            print("Product deleted successfully")  # Debug log
            
            # Delete the associated image file if it exists
            if image_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    print("Image file deleted successfully")  # Debug log
                except Exception as e:
                    print(f"Error deleting image file: {e}")
            
            return Response({'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)
            
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_products(request):
    if request.method == "POST":
        try:
            user = Product.objects.get(id=request.data.get('id'))
            user.name = request.data.get('name')
            user.productid = request.data.get('productid')
            user.category = request.data.get('category')
            user.price = request.data.get('price')
            user.stock = request.data.get('stock')
            user.sales = request.data.get('sales')
            user.image = request.FILES.get('image')
            user.save()
            return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)
