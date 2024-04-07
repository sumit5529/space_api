from rest_framework import generics,viewsets
from .models import Product, Customer, Bill,BillProduct
from .serializers import ProductSerializer, CustomerSerializer, BillSerializer,UserRegistrationSerializer


from django.db.models import Sum, Count
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

class UserRegistrationAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

# Product Views
class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Customer Views
class CustomerListCreate(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
# Product Views
class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Customer Views
class CustomerListCreate(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

from rest_framework.permissions import IsAuthenticated
class BillListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Bill.objects.all()
    # queryset = Bill.objects.prefetch_related('products')
    serializer_class = BillSerializer

class BillDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

class SalesAnalyticsAPIView(APIView):
    def get(self, request):
        top_selling_products = Product.objects.annotate(total_sold=Sum('billproduct__quantity')).order_by('-total_sold')[:5]
        top_employees_by_sales = User.objects.annotate(total_sales=Count('bill')).order_by('-total_sales')[:5]
        
        top_selling_products_data = [{'name': product.name, 'total_sold': product.total_sold} for product in top_selling_products]
        top_employees_by_sales_data = [{'employee': user.username, 'total_sales': user.total_sales} for user in top_employees_by_sales]
        
        return Response({
            'top_selling_products': top_selling_products_data,
            'top_employees_by_sales': top_employees_by_sales_data
        })