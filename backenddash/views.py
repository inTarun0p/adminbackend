from os import name
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .Serializer import UserSerializer
# Create your views here.
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User created successfully', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'error': 'Invalid data', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
       try:
           user = User.objects.get(email=request.data['email'])
           if user.password == request.data['password']:
           
            return Response(
                   {'message': 'Login successful', 'data': {'name': user.name, 'email': user.email}},
                   status=status.HTTP_200_OK
               )
           return Response(
               {'error': 'Invalid credentials'},
               status=status.HTTP_401_UNAUTHORIZED
           )
       except User.DoesNotExist:
           return Response(
               {'error': 'User not found'},
               status=status.HTTP_404_NOT_FOUND
           )


@api_view(['GET'])
def view_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        count = User.objects.count()
        serializer = UserSerializer(users, many=True)
        return Response({'count': count, 'data': serializer.data})
    return Response(
        {'error': 'Invalid request method'},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
def delete_user(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.data.get('id'))
        user.delete()
        return Response(
            {'message': 'User deleted successfully'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'error': 'Invalid request method'},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
def update_user(request):
    try:
        id = request.data.get('id')

        if not id or id == 'undefined':
            return Response({'error': 'Invalid or missing ID'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=int(id))

        user.name = request.data.get('name')
        user.email = request.data.get('email')
        user.password = request.data.get('password')
        user.country = request.data.get('country')
        user.mobile = request.data.get('mobile')
        user.save()

        return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
