from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSeralizers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Swagger dependencies
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='POST',request_body=DrinkSeralizers)
@api_view(['GET','POST'])
def drink_list(request,format=None):
    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSeralizers(drinks,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = DrinkSeralizers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PUT',request_body=DrinkSeralizers)       
@api_view(['GET','PUT','DELETE'])
def drink_detail(request,id,format=None):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = DrinkSeralizers(drink)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = DrinkSeralizers(drink,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        drink.delete()
        return Response({"Message":"Drink Deleted."},status=status.HTTP_204_NO_CONTENT)