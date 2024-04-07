

from rest_framework import serializers
from .models import Product, Customer, Bill, BillProduct
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price','stock_quantity']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class BillProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)  # To allow specifying product by ID

    class Meta:
        model = BillProduct
        fields = ['product', 'product_id', 'quantity']
        # Removed the `print(product)` statement as it's not appropriate here

class BillSerializer(serializers.ModelSerializer):
    products = BillProductSerializer(source='billproduct_set', many=True, required=False)  # Correct relation access
    print(products)
    class Meta:
        model = Bill
        fields = ['id','customer','total_amount', 'billed_by', 'date', 'products']
    
    def create(self, validated_data):
        products_data = validated_data.pop('billproduct_set', [])
        bill = Bill.objects.create(**validated_data)
        for product_data in products_data:
            BillProduct.objects.create(bill=bill, **product_data)
        bill.update_total_amount()  # Ensure this method correctly calculates total_amount
        return bill

    def update(self, instance, validated_data):
        products_data = validated_data.pop('billproduct_set', [])
        BillProduct.objects.filter(bill=instance).delete()  # Simplified: Deletes existing products, could be optimized

        for product_data in products_data:
            BillProduct.objects.create(bill=instance, **product_data)
        
        instance.update_total_amount()  # Recalculate total_amount after update
        return super().update(instance, validated_data)

