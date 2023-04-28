from django.shortcuts import render,redirect
from django.db.models import Count
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from .forms import *
from django.contrib import messages
from .models import *
import razorpay
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
UserModel = get_user_model()

from .tokens import account_activation_token


# Create your views here.
class PageTitleMixin(object):
    def get_page_title(self, context):
        return getattr(self, "title", "Default Page Title")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_page_title(context)
        return context
    
@login_required
def home(request):
    context={
        'title':"Home",
    }
    return render(request, 'app/home.html', context)

@login_required
def about(request):
    context={
        'title':"About Us"
             }
    return render(request, 'app/about.html', context)

@login_required
def contact(request):
   
    context={'title':"Contact Us"}
    return render(request, 'app/contact.html', context)


class CategoryView(PageTitleMixin,View):
    def get(self,request,value):
        product=Product.objects.filter(category=value)
        title=value
        print('title = ', title)
        return render(request,"app/category.html",locals())


class ProductDetail(PageTitleMixin,View):
        title='Product Detail'
        def get(self,request,pk):
            product=Product.objects.get(pk=pk)
            wishlist=Wishlist.objects.filter(Q(user=request.user) & Q(product=product))
            title=product
            print("Product=",product)
            print("Wishlist=",wishlist)
            return render(request,'app/product_detail.html',locals())
# @csrf_exempt
# def verifyEmail(request):
#     if request.method == 'POST':
#         user_otp=request.POST.get('otp')
#         name=request.POST.get('name')
#         email=request.POST.get('email')
#         password1=request.POST.get('password1')
#         password2=request.POST.get('password2') 
        
#         if password1 == password2:
#           form=CustomUser(name=name,email=email,password1=password1)  
#           form.save()
#         print("User OTP=",user_otp)
#     return JsonResponse({'data':"Verify email"},status=200) 
        
class Registration(PageTitleMixin,View):
    success_url=reverse_lazy('/accounts/login') 
    def get(self,request):
        form= RegistrationForm()
        title='Registration'
        return render(request,'app/registration.html',locals())
    
    def post(self,request):
        form= RegistrationForm(request.POST)
        title='Registration'
        name=request.POST.get('name')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2') 
        
        if form.is_valid():
            # otp=random.randint(100000,999999)
            # subject = 'Email Verification'
            # message = f'Hi Verify your email adress by OTP : {otp} .'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [email, ]
            # send_mail( subject, message, email_from, recipient_list )
            user= form.save(commit=False)
            user.is_active=False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('app/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = [email,]
            email = EmailMessage(
                mail_subject, message, to_email
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = RegistrationForm()
        return render(request, 'app/registration.html', {'form': form})
        #     messages.success(request,"User register Successfully")
        #     return render(request,'app/verify.html',context)
        # else:
        #     messages.warning(request,"Enter Valid data")
        # return render(request, 'app/registration.html',locals())  
    
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
              
class ProfileView(View):
    def get(self,request):
        prev_add=Customer.objects.filter(user=request.user).first()
        form=ProfileForm(instance=prev_add)
        title='Profile'
        return render(request,'app/profile.html',locals())
    
    def post(self,request):
        form=ProfileForm(request.POST)
        title='Profile'
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']  

            customer=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,
                         state=state,zipcode=zipcode)
            customer.save()
            messages.success(request,"Profile saved Successfully!")
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request,'app/profile.html',locals())
    
@login_required    
def address(request):
    address_obj=Customer.objects.filter(user=request.user)
    title='Address'
    return render(request,'app/address.html',locals())

class UpdateAddress(View):
    page_title='UpdateAddress'
    def get(self,request,pk):
        prev_add=Customer.objects.get(pk=pk)
        form=ProfileForm(instance=prev_add)
        return render(request,'app/update_address.html',locals())
        
    def post(self,request,pk):
        form=ProfileForm(request.POST)
        if form.is_valid():
            new_address=Customer.objects.get(pk=pk)
            new_address.name=form.cleaned_data['name']
            new_address.locality=form.cleaned_data['locality']
            new_address.city=form.cleaned_data['city']
            new_address.mobile=form.cleaned_data['mobile']
            new_address.state=form.cleaned_data['state']
            new_address.zipcode=form.cleaned_data['zipcode']  
            new_address.save()
            messages.success(request,"Profile updated Successfully!")
        else:
            messages.warning(request,'Invalid Input Data')
        return redirect('address')
    
def delete_address(request,pk):
    title='Address'
    address=Customer.objects.get(pk=pk)
    address.delete()
    return redirect('address')
    
@login_required    
def add_to_cart(request):
    title='Cart'
    user=request.user
    product_id=request.GET.get('product_id')
    product_req_to_add =Product.objects.get(id=product_id)
    print("product_req_to_add = ", product_req_to_add)

    cart = Cart.objects.all().filter(user = user)
    print("cart=",list(cart))
    
    product_list  = list(cart.values('product__title'))
    print("list of products in cart=",product_list )
    
    names_of_product = [d['product__title'] for d in product_list]
    names_of_product = []
    for d in product_list:
        names_of_product.append(d['product__title'])
    print("names_of_product = ", names_of_product)
    
    if str(product_req_to_add) in names_of_product:
        print("inside if")
        cart_obj = Cart.objects.get(product__title = str(product_req_to_add))
        cart_obj.quantity += 1
        cart_obj.save()
    else:
        print("inside else")
        Cart(user=user, product=product_req_to_add).save()
    
    print("*"*20)
    return redirect('/cart')
    
@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    title='Cart'
    amount=0
    for p in cart:
        if p.quantity > 0:
            value=p.quantity * p.product.discounted_price
            amount += value
            totalamount=amount+ 40
    
    return render(request,'app/add_to_cart.html',locals())

class checkout(View):
    def get(self,request):
       
        user=request.user
        address=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        title='Place Order'
        final_amt=0
        for p in cart_items:
            value=p.quantity * p.product.discounted_price
            final_amt += value
        totalamount=final_amt+ 40
        razoramount=int(totalamount*100)
        
        client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data={'amount':razoramount,'currency':"INR"}                      
        payment_response=client.order.create(data=data)  
        print(payment_response)
        
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status == 'created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )   
            payment.save()              
        return render(request,'app/checkout.html',locals())
    
@login_required    
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    print('paymentdone: oid=',order_id,'pid=',payment_id,'cid=',cust_id)
    title='PaymentDone' 
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    
    #To UPDATE payment status and payment id
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    
    #To SAVE Order details
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect('/orders')
  
@login_required
def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    title='Orders'
    return render(request,'app/orders.html',locals())

@login_required
def plus_cart(request):
    pass
    if request.method == "GET":
        product_id=request.GET['product_id']
        c=Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discounted_price
            amount += value
        totalamount=amount+ 40
        data={ 
              'quantity':c.quantity,
              'amount':amount,
              'totalamount':totalamount     
        }
    return JsonResponse(data)

@login_required
def minus_cart(request):
    pass
    if request.method == "GET":
        product_id=request.GET['product_id']
        c=Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            if p.quantity !=0:
                value=p.quantity * p.product.discounted_price
                amount += value
                totalamount=amount+ 40
            else:
                totalamount=amount+0    
        
        data={ 
              'quantity':c.quantity,
              'amount':amount,
              'totalamount':totalamount     
        }
    return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == "GET":
        product_id=request.GET['product_id']
        c=Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.delete()
        
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discounted_price
            amount += value
        totalamount=amount+ 40
        
        data={ 
              'amount':amount,
              'totalamount':totalamount     
        }
    return JsonResponse(data)

@login_required
def plus_wishlist(request):
    if request.method == "GET":
        product_id=request.GET['product_id']
        product=Product.objects.get(id=product_id)
        user=request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'added to wishlist!'
        }
        return JsonResponse(data)
    
@login_required    
def minus_wishlist(request):
    if request.method == "GET":
        product_id=request.GET['product_id']
        product=Product.objects.get(id=product_id)
        user=request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'removed from wishlist!'
        }
        return JsonResponse(data)    
    
    
@login_required    
def search(request):
    query=request.GET['search']
    product=Product.objects.filter(Q(title__icontains=query))
    if len(query) == 0:
        messages.warning(request,"No product found")
    if len(product) == 0:
        messages.warning(request,"NOT Available!")
    title='Search'        
    return render(request,'app/search.html',locals())

def wishlist(request):
    user=request.user
    product=Wishlist.objects.filter(user=user)
    return render(request,'app/wishlist.html',locals())