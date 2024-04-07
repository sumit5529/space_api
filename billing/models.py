
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.IntegerField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name


class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='BillProduct')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    billed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill {self.id} - {self.customer.name}"
    def update_total_amount(self):
        try:
            total_amount = sum(bill_product.subtotal() for bill_product in self.billproduct_set.all())
            self.total_amount = total_amount
            self.save()
        except Exception as e:
            print("error during updating total amount")

class BillProduct(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def subtotal(self):
      return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.bill.update_total_amount()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.bill.update_total_amount()
    

