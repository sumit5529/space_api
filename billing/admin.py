from django.contrib import admin
from .models import Product, Customer, Bill, BillProduct

class BillProductInline(admin.TabularInline):
    model = BillProduct
    extra = 1  # Number of extra forms to display

class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'billed_by', 'date')
    list_filter = ('date', 'billed_by')
    inlines = [BillProductInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity')
    search_fields = ('name',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name', 'email')

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Bill, BillAdmin)
