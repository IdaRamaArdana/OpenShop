from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Product
from .serializers import ProductSerializer

class ProductList(APIView):
    def get(self, request):
        # Mengambil query parameter untuk fitur pencarian (Untuk Kriteria 5)
        name_query = request.query_params.get('name', None)
        location_query = request.query_params.get('location', None)

        # Hanya menampilkan produk yang belum di-soft delete di list utama
        products = Product.objects.filter(is_delete=False)

        # Melakukan filter berdasarkan parameter pencarian yang dikirim (case-insensitive)
        if name_query:
            products = products.filter(name__icontains=name_query)
        if location_query:
            products = products.filter(location__icontains=location_query)

        # Return list kosong (products: []) jika tidak ada data yang cocok
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Otomatis mengembalikan status 400 jika data tidak valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            # Produk yang sudah di-soft delete tetap bisa diakses melalui ID (Untuk Kriteria 4 Advanced)
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            product = self.get_object(pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            product = self.get_object(pk)
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = self.get_object(pk)
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # Mengimplementasikan Soft Delete
        product.is_delete = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)