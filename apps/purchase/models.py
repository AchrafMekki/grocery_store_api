from django.db import models
from django.contrib.auth.models import User
from apps.product.models import Product



class Order(models.Model):
    order_transaction = models.IntegerField()
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    product_id = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    purchase_date = models.DateField()
    quantity = models.IntegerField()
    purchase_cost =  models.DecimalField(max_digits=6, decimal_places=2)
     #Integerfield?
    class Meta:
        unique_together = ('order_transaction', 'customer_id', 'product_id')

 
    def __str__(self):
        return f'Order: {self.order_transaction}, Customer: {self.customer_id}, Date: {self.purchase_date}'



class Cart(models.Model):
    customer_id=models.ForeignKey('customer.Customer',on_delete=models.CASCADE)
    product_id=models.ForeignKey('product.Product',on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def get_cost_per_product(self):
        return self.product_id.price
    
    def get_total_amount(self):
        return  self.quantity * self.product_id.price
    
    def __str__(self):
        return f'Customer ID : {self.customer_id}, Product ID : {self.product_id}, QTY {self.quantity}'
    
class PaymentStatus(models.TextChoices):
    PAID = 'PAID'
    UNPAID = 'UNPAID'

class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing',
    SHIPPED = 'Shipped',
    DELIVERED = 'Delivered'

class PaymentMethod(models.TextChoices):
    COD ='COD'
    CARD = 'CARD'
    PAYPAL = 'PAYPAL'



class OrderTest(models.Model):
    street = models.CharField(max_length=500, default="", blank=False)
    city = models.CharField(max_length=100, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    phone_no = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    total_amount = models.IntegerField(default=0)
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID
    )
    status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CARD
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
class ItemTest(models.Model): # Shopping Cart
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(OrderTest, on_delete=models.CASCADE, null=True, related_name="orderitems")
    name = models.CharField(max_length=200, default="", blank=False)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)

    def __str__(self):
        return str(self.name)
    

