from django.db import models
from django.shortcuts import reverse

from django.conf import settings
# Create your models here.
CATEGORY_CHOICES = (
    ('M','Mobile'),
    ('L','Laptop'),
    ('T','Tv'),
    ('C','Cloth')
)
LABEL_CHOICES = (
    ('P','Primary'),
    ('S','Secondary'),
    ('D','Denger')
)

class Product(models.Model):
    photo = models.ImageField(upload_to='productphoto')
    name = models.CharField(max_length=50)
    des = models.TextField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=10)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1)
    slug = models.SlugField()
    


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("app1:product", kwargs={"slug": self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("app1:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("app1:remove-from-cart", kwargs={"slug": self.slug})
        

class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    
    

    def __str__(self):
        return f"{self.qty} or {self.product.name}"
    
    def get_total_product_price(self):
        return self.qty * self.product.price

    def get_total_discount_product_price(self):
        return self.qty * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_discount_product_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_amount_saved()
        return self.get_total_product_price()
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
    
    
    def get_total(self):
        total = 0
        
        for order_product in self.products.all():
            total += order_product.get_final_price()
        
        return total

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code
    