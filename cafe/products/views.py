from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ProductList(APIView):
    permission_classes = [IsAuthenticated]

    """
    List all products or create a new product.
    """
    def get(self, request, format=None):
        name_query = request.query_params.get('name')
        if name_query:
            products = ProductFilter(request.query_params, queryset=Product.objects.all()).qs
        else:
            products = Product.objects.all()
        
        paginator = Paginator(products, 10)
        cursor = request.query_params.get('cursor')

        if cursor is not None:
            try:
                products = paginator.page(cursor)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
        else:
            products = paginator.page(1)

        serializer = ProductSerializer(products, many=True)
        data = {
            'count': paginator.count,
            'next_cursor': str(products.next_page_number()) if products.has_next() else None,
            'prev_cursor': str(products.previous_page_number()) if products.has_previous() else None,
            'results': serializer.data
        }
        return Response(data)
    


class ProductDetail(APIView):
    permission_classes = [IsAuthenticated]
    """
    Retrieve, update or delete a product instance.
    """
    def get_object(self, pk):
        try:
            product = Product.objects.get(pk=pk)
            if product.account != self.request.user:
                raise Http404
            return product
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.copy()
        data['account'] = request.user.id
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductUpdate(APIView):
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PATCH']
    """
    Update the specified product.
    """
    def get_object(self, pk):
        try:
            product = Product.objects.get(pk=pk)
            if product.account != self.request.user:
                raise Http404
            return product
        except Product.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDelete(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        if not request.user == product.account:
            raise PermissionDenied
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
