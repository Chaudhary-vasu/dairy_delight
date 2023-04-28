from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser,PermissionsMixin
# from django.utils.translation import ugettext_lazy
from app.managers import CustomUserManager
# Create your models here.

STATE_CHOICES = (
   ("AN","Andaman and Nicobar Islands"),
   ("AP","Andhra Pradesh"),
   ("AR","Arunachal Pradesh"),
   ("AS","Assam"),
   ("BR","Bihar"),
   ("CG","Chhattisgarh"),
   ("CH","Chandigarh"),
   ("DN","Dadra and Nagar Haveli"),
   ("DD","Daman and Diu"),
   ("DL","Delhi"),
   ("GA","Goa"),
   ("GJ","Gujarat"),
   ("HR","Haryana"),
   ("HP","Himachal Pradesh"),
   ("JK","Jammu and Kashmir"),
   ("JH","Jharkhand"),
   ("KA","Karnataka"),
   ("KL","Kerala"),
   ("LA","Ladakh"),
   ("LD","Lakshadweep"),
   ("MP","Madhya Pradesh"),
   ("MH","Maharashtra"),
   ("MN","Manipur"),
   ("ML","Meghalaya"),
   ("MZ","Mizoram"),
   ("NL","Nagaland"),
   ("OD","Odisha"),
   ("PB","Punjab"),
   ("PY","Pondicherry"),
   ("RJ","Rajasthan"),
   ("SK","Sikkim"),
   ("TN","Tamil Nadu"),
   ("TS","Telangana"),
   ("TR","Tripura"),
   ("UP","Uttar Pradesh"),
   ("UK","Uttarakhand"),
   ("WB","West Bengal")
)

CATEGORY_CHOICES=(
    ('Curd','Curd'),
    ('Milk','Milk'),
    ('Lassi','Lassi'),
    ('Milkshake','Milkshake'),
    ('Paneer','Paneer'),
    ('Ghee','Ghee'),
    ('Cheese','Cheese'),
    ('Ice-creams','Ice-Creams'),
)
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField(default='',blank=True)
    prodapp=models.TextField(default='',blank=True)
    category=models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    product_image=models.ImageField(upload_to='product')
    
    def product_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.product_image.url))
    product_photo.short_description = "Products Image"
    product_photo.allow_tags = True

    
    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser,PermissionsMixin):
    username = None
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Meta(AbstractUser.Meta):
    swappable = 'AUTH_USER_MODEL'    
    
   
class Customer(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    # email=models.EmailField(unique=True,default='')
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200,blank=True)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.CharField(max_length=100,blank=True)
    state=models.CharField(choices=STATE_CHOICES,max_length=100)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    class Meta:
        verbose_name_plural='Cart'
        verbose_name=('CART')
    
STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
    )

    
class Payment(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)
    
class OrderPlaced(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='On the way')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE, default="")
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    