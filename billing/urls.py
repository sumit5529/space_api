from django.urls import path
from .views import (ProductListCreate, ProductDetail, 
                    CustomerListCreate, CustomerDetail, 
                    SalesAnalyticsAPIView, 
                    BillListCreate, BillDetail,UserRegistrationAPIView)
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # Product URLs
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('products/', ProductListCreate.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    
    # Customer URLs
    path('customers/', CustomerListCreate.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
    
    # Bill URLs
    path('bills/', BillListCreate.as_view(), name='bill-list'),
    path('bills/<int:pk>/', BillDetail.as_view(), name='bill-detail'),
    
    # Sales Analytics URL
    path('sales-analytics/', SalesAnalyticsAPIView.as_view(), name='sales-analytics'),
    # Add other URLs as needed
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
