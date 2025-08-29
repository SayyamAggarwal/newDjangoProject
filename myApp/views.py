from django.shortcuts import render,redirect,get_object_or_404
from myApp.models import *
from django.conf import settings 
from django.core.mail import send_mail
import pandas as pd
from django.shortcuts import render 
from django.http import JsonResponse
import json 
import razorpay 
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def footer2(request):
    return render(request,'footer2.html')
def contact_us(request):  
    if request.method == "POST":
        x = contactus()  
        x.name = request.POST.get('nm')
        x.email = request.POST.get('em')
        x.phonenumber = request.POST.get('ph')
        x.message = request.POST.get('msg') 
        x.save()
        return render(request, 'contact us.html', {'success': True})
    return render(request, 'contact us.html')

  
def sample(request):
    if request.method=="POST":
        x=sam()
        x.title=request.POST.get('t')
        x.msg=request.POST.get('m')
        x.save()
        return render(request,'sample.html',{'msg':"data successfully added"})
    else:
        return render(request, 'sample.html')



def register(request):
 if request.method=="POST":
     em=request.POST.get('e')   
     pw=request.POST.get('p')
     cpw=request.POST.get('c')
     if pw==cpw:
               if userregister.objects.filter(email=em).exists():
                return render(request,'register.html',{'msg':"email  is already registered"})
               else:
                   a=userregister()
                   a.name=request.POST.get('n')
                   a.email=request.POST.get('e')
                   a.password=request.POST.get('p')
                   a.save()
                   return render(request,'register.html',{'msg':"user successfully registered"})
     else: 
        return render(request,'register.html',{'msg':"password and confirm password does not match"})
 else:
      return render(request,'register.html') 


def login(request):
    if request.method=="POST":
          em=request.POST.get('e')   
          pw=request.POST.get('p')
          data=userregister.objects.filter(email=em, password=pw)
          if len(data)>0:
              request.session['email']=em
              return redirect('/home_page/')
          else:
               return render(request,'login.html',{'msg':"invalid email , password"})
    else:
        return render(request,'login.html')
        
def userprofile(request):
    user=userregister.objects.get(email=request.session['email'])
    return render(request,'profile.html',{'user':user})

def Allproducts(request):
    cat=category.objects.all()
    x=Product.objects.all()
    
    return render(request,'Allproducts.html',{'data':x,'cat':cat})


def filterproducts(request, name):
    cat=category.objects.all()
    x=Product.objects.filter(category=name)
    
    return render(request,'Allproducts.html',{'data':x,'cat':cat})
              
              
def detail(request,id):  
        user_data=userregister.objects.get(email=request.session['email'])   
        user=user_data
        cat=category.objects.all()
                 
        x=Product.objects.get(id=id)
        return render(request,'detail.html',{'data':x,'cat':cat})
    
def add_to_cart(request):
    if request.method=="POST":
        print("working")
        user_data=userregister.objects.get(email=request.session['email'])
        user=user_data
        cat=category.objects.all()
        product_id=request.POST.get('Product')
        product=Product.objects.get(id=product_id)
        cart(user=user_data, product=product).save()
        print("-----------working-----------")
        return redirect('/show_add_to_cart')
        return render(request,'showaddtocart.html',{'cat':cat})
        

def show_add_to_cart(request):
    user_data=userregister.objects.get(email=request.session['email'])
    user=user_data
    cat=category.objects.all()
    all_data=cart.objects.filter(user=user, payment_id__isnull=True) #cart will get empty because of isnull after order
    total=0
    for i in all_data:
        total=total+(i.product.price* i.quantity)
    print(total)
    shipping_charges=50
    grandtotal=total+shipping_charges
    return render(request,'showaddtocart.html',{'cart_data':all_data, 'grandtotal':grandtotal,'tot':total, 'cat':cat}) 


# Increment Quantity
def increment_quantity(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(cart, id=item_id)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('/show_add_to_cart')  # Redirect to cart page or any desired page

# Decrement Quantity
def decrement_quantity(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(cart, id=item_id)
        
        # Ensure quantity does not go below 1
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
    
    return redirect('/show_add_to_cart')  # Redirect to cart page or any desired page
 
#  remove item from cart
def remove_item(request, item_id):
    if request.method =="POST":
        cart_item = get_object_or_404(cart, id=item_id)
        cart_item.delete()  #remove the item from the cart
        return redirect ('/show_add_to_cart')

def clear_cart(request):
    if request.method=="POST":
        # get user's cart
        user_data=userregister.objects.get(email=request.session['email'])
        allcartdata=cart.objects.filter(user=user_data)
        # clear all items
        for single in allcartdata:
            single.delete()
        return redirect('/show_add_to_cart')
    
    # Initialize Razorpay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_order(request):
    user_data = userregister.objects.get(email=request.session['email'])
    user = user_data
    all_data = cart.objects.filter(user=user)
    amount = 0
    for i in all_data:
        single_cost = int(i.quantity) * int(i.product.price)
        amount += single_cost
    total_amount = amount + 30
    return render(request, "payment.html", {
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        'amount': total_amount
    })


@csrf_exempt
@csrf_exempt
def save_payment(request):
    print('enter')
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            print("enter try block")
            data = json.loads(request.body)
            payment_id = data.get("payment_id")
            amount = data.get("amount")*100
            status = data.get("status")
            print("fetch all data", payment, amount, status)
            # Fetch the user data using session email
            user_data= userregister.objects.get(email=request.session['email'])  #
            user = user_data
                        # Get all the cart items for the user
            all_data = cart.objects.filter(user=user)


            # Save payment details to the Payment model
            pay = payment.objects.create(payment_id=payment_id, amount=amount, status=status, user=user)
            # pay.save()
            print("saved payment")
            

            # Update cart items with the payment_id
            for cart_item in all_data:
                # Directly access the cart_id (no need for get() method)
                cart_item.payment_id = payment_id  # Assign the payment ID to the cart
                cart_item.save()
            

            # return redirect('/success_page')
            return JsonResponse({"message": "Payment saved successfully"}, status=200)
       
        except userregister.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=400)
       
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
   
    return JsonResponse({"error": "Invalid request method"}, status=405)

def shipping_address_view(request):
        user_data = userregister.objects.get(email=request.session['email'])
        user=user_data
        cat=category.objects.all()
        if request.method == "POST":
      
            x =ShippingAddress()
            x.user = user_data
            x.name = request.POST.get('user')
            x.pincode = request.POST.get('pincode')
            x.country = request.POST.get('country')
            x.email = request.POST.get('email')
            x.phone = request.POST.get('phoneno')
            x.state = request.POST.get('state')
            x.address = request.POST.get('address')
            
            x.save()
            print("succ")
            return redirect('/check_out')
       
        else:
         return render(request, "shipping.html", {'cat':cat})

      
                                   
def check_out(request):
    user_data=userregister.objects.get(email=request.session['email'])
    user=user_data
    cat=category.objects.all()
    all_data=cart.objects.filter(user=user)
    total=0
    for i in all_data:
        total=total+(i.product.price* i.quantity)
    print(total)
    shipping_charges=50
    grandtotal=total+shipping_charges
    x=ShippingAddress.objects.filter(user=user_data).last()
    return render(request,'checkout.html',{'cart_data':all_data, 'grandtotal':grandtotal,'tot':total,'add':x,'cat':cat})
        

def success_page(request):
       return render(request, 'success.html')



def my_orders(request):
    # Assuming you store user ID in session after login
    user_id = userregister.objects.get(email=request.session['email'])
    if not user_id:
        # Redirect to login page if user is not logged in
        return redirect('login')

    # Get all carts with payment_id (i.e., orders) for this user
    orders = cart.objects.filter(user=user_id, payment_id__isnull=False)

    context = {
        'orders': orders
    }
    return render(request, 'myorder.html', context) 

def forgot_password(request):
    if request.method == 'POST':
        e = request.POST.get('e')
        user = userregister.objects.filter(email=e)
        length = len(user)
        if length > 0:
            pw = user[0].password
            subject = "password"
            message = "Welcome to Dhawan's furniture\nYour Password is " + pw
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e]
            send_mail(subject, message, email_from, recipient_list)
            msg = "Your Password sent to your respective Email Account, Please check your Email"
            return render(request, 'forgotpass.html', {'msg': msg})
        else:
            return render(request, 'forgotpass.html', {'msg': "This Email is not registered"})
    else:
        return render(request, 'forgotpass.html')
    
def home_page(request):
    return render(request,'home.html')
    



