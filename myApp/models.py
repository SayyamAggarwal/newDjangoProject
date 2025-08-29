from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class demo(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    
class category(models.Model):
    category=models.CharField(max_length=100,primary_key=True)
    
    def __str__(self):
        return self.category
        
class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveBigIntegerField()
    company=models.CharField(max_length=100)
    image = models.CharField(max_length=200) 
    
    
class sam(models.Model):
    title=models.CharField(max_length=1000)   
    msg=models.TextField()   
    
class userregister(models.Model):
    name=models.CharField(max_length=1000) 
    email=models.EmailField()
    password=models.CharField(max_length=1000)
    
class cart(models.Model):
    
    
    # links to user who owns the cart
    user=models.ForeignKey(userregister, on_delete=models.CASCADE)
    # link to product
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    # quantity of product in cart
    quantity= models.PositiveIntegerField(default=1)
    # when product was added to cart
    added_at= models.DateTimeField(auto_now_add=True) 
    
    payment_id=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return f"{self.user.name}'s cart - {self.product.name}"
    
    # Assuming product_price is stored as a string but represents a float
    def total_price(self):
        return float(self.product.price) * self.quantity
    
    
    
class payment(models.Model):
        user=models.ForeignKey(userregister,on_delete=models.CASCADE)
        payment_id=models.CharField(max_length=100,unique=True,primary_key=True)
        amount=models.IntegerField()
        status=models.CharField(max_length=50)
        created_at=models.DateTimeField(auto_now_add=True)
        def __str__(self):
            return self.payment_id
     




class ShippingAddress(models.Model):
    user = models.ForeignKey(userregister, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    state = models.CharField(max_length=100)
    address = models.TextField()


    def __str__(self):
        return f"{self.name} - {self.address}"
    

    
class Order(models.Model):
    User = get_user_model()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    
class contactus(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField()
    phonenumber=models.CharField(max_length=30)

