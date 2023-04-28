from app.models import *
from .forms import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','category','product_photo']
    search_fields=['id','title','selling_price','discounted_price','category']
    
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['user','locality','city','state','zipcode']
    search_fields=['locality','city','state','zipcode']
    
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
    search_fields=['quantity']
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
    search_fields=['amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
    
@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
        list_display=['user','customer','product','quantity','ordered_date','status','payment']
        search_fields=['quantity','ordered_date','status','payment']
        
        
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
            list_display=['user','product']
        
# admin.site.unregister(User)
# admin.site.register(CustomUser,CustomUserAdmin)