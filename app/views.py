from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from .forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm
from .forms import InflencerLoginForm, InfluencerSignUpForm, InfluencerRegistrationForm, InfluencerLoginForm, MyPasswordChangeForm
from django.db import connection
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView
# from .forms import MyPasswordReserForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.http import HttpResponse

# Create your views here.




from .forms import SellerForm
# Create your views here.

@login_required
def addProduct(request):
    influencercode = request.session.get('influencercode')
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Assign the current user to the product
            product.save()
            print("Data saved successfully")
            return redirect('addproduct')
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = SellerForm()

    queryset = Product.objects.filter(user=request.user)  # Fetch products for the current user
    context = {'form': form, 'influencercode': influencercode, 'queryset': queryset}
    return render(request, 'app/seller.html', context)


def delete_Product(request, id):
   queryset = Product.objects.get(id=id)
   queryset.delete()
   return redirect('addproduct')

def insta(request):
    influencercode = request.session.get('influencercode')
   
    return render(request, 'app/instagram.html', {'influencercode':influencercode})

def password_change_view(request):
    influencercode = request.session.get('influencercode')
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # You can customize the success URL or use reverse to dynamically generate it
            return redirect('/passwordchangedone/')
    else:
        form = MyPasswordChangeForm(request.user)

    return render(request, 'app/passwordchange.html', {'form': form, 'influencercode':influencercode})

def influencer_password_change_view(request):
    influencercode = request.session.get('influencercode')
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # You can customize the success URL or use reverse to dynamically generate it
            return redirect('/passwordchangedone2/')
    else:
        form = MyPasswordChangeForm(request.user)

    return render(request, 'app/influencerpasswordchange.html', {'form': form, 'influencercode':influencercode})

def password_change_done(request):
    # Get the influencer code from the session
    influencercode = request.session.get('influencercode')

    # You can customize the template_name and other logic as needed
    context = {'influencercode': influencercode}
    return redirect('login')

    return render(request, 'app/passwordchangedone.html', context)

def influencer_password_change_done(request):
    # Get the influencer code from the session
    influencercode = request.session.get('influencercode')

    # You can customize the template_name and other logic as needed
    context = {'influencercode': influencercode}
    return redirect('influencerlogin')
    return render(request, 'app/influencerpasswordchangedone.html', context)


@login_required
def returnpro(request):
 if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('prod_id')
        reason = request.POST.get('reason')
        product = Product.objects.get(id=product_id)
        print(product.id)

        if Return.objects.filter(user=user, product__id=product_id).exists():
         messages.warning(request, 'This query has not submitted, because you have already raised return request .')
         
        else: 
         Return(user=user, product=product, reason=reason).save()
         messages.success(request, 'Return request raised successfully.')

 return redirect('/orders')

@login_required
def profile(request):
  influencercode = request.session.get('influencercode')
 
  return render(request, 'app/profile.html', {'influencercode':influencercode})

def aboutus(request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/aboutus.html', {'influencercode':influencercode,'totalitem':totalitem})

def influencer_rules(request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/influencer_rules.html', {'influencercode':influencercode,'totalitem':totalitem})

def aboutus2(request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
  if request.user.is_authenticated:
     totalitem = len(InfluencerCart.objects.filter(user=request.user))

  return render(request, 'app/influencerabout.html', {'influencercode':influencercode,'totalitem':totalitem})

@login_required
def contactus(request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))

  return render(request, 'app/contactus.html', {'influencercode':influencercode,'totalitem':totalitem})

@login_required
def contactus2(request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
  if request.user.is_authenticated:
     totalitem = len(InfluencerCart.objects.filter(user=request.user))

  return render(request, 'app/influencercontact.html', {'influencercode':influencercode,'totalitem':totalitem})

###########Logic for Email sent start###################

def sendmail(request):
 influencercode = request.session.get('influencercode')
 if request.method == 'POST':
    name = request.POST['name']
    email = request.POST['email']
    contact = request.POST['contact']
    user = request.user
    user2 = request.user.email
    print(user)
    print(user2)
    print("jendonocjn")
    # print(first_name)
    message = request.POST['message']
    data1 = {'Name': name, 'Email': email}
    data2 = {'Phone_No': contact, 'Message':message}

    message_body = f"Name: {name}\nEmail: {email}\nPhone_No: {contact}\nMessage: {message}"
    send_mail(
        "CLOTHEE USER",
        message_body,
        "hari638241@gmail.com",  # login user email or Host email
        ["hari638241@gmail.com"], # admin email
        fail_silently=False,
    )
    messages.info(request, "Mail send Successfully")
    return render(request, 'app/contactus.html', {'influencercode':influencercode})
 else:
    messages.info(request, "Mail Not send")
    return render(request, 'app/contactus.html', {'influencercode':influencercode})
 
 ###############Logic for email send Finish

from django.core.exceptions import ObjectDoesNotExist
def activate(request, uidb64, token):
    User = get_user_model()
    try:
       uid = force_str(urlsafe_base64_decode(uidb64))
       user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
       user=None
    if user is not None and account_activation_token.check_token(user, token):
       user.is_active = True
       user.save()
       return render(request, 'app/emailconfirm.html')
    else:
       return HttpResponse('Activation link is invalid')
 

# def change_password(request):
#   return render(request, 'app/passwordchange.html')


class ProductView(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears, 'Tshirts':Tshirts, 'influencercode':influencercode, 'totalitem':totalitem})

class BottomWear(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/bottomwears.html',{ 'bottomwears':bottomwears,  'influencercode':influencercode, 'totalitem':totalitem})

class TopWear(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
  topwears = Product.objects.filter(category='TW')
#   bottomwears = Product.objects.filter(category='BW')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/topwears.html',{ 'topwears':topwears,  'influencercode':influencercode, 'totalitem':totalitem})

class Tshirts(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
#   bottomwears = Product.objects.filter(category='BW')
  Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/tshirt.html',{ 'Tshirts':Tshirts,  'influencercode':influencercode, 'totalitem':totalitem})
 
class MensWear(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  MTH = Product.objects.filter(category='MTH')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/MTH.html',{ 'MTH':MTH,  'influencercode':influencercode, 'totalitem':totalitem})

class MensWear1(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  MSC = Product.objects.filter(category='MSC')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/MSC.html',{ 'MSC':MSC,  'influencercode':influencercode, 'totalitem':totalitem})
 
class MensWear2(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  MPS = Product.objects.filter(category='MPS')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/MPS.html',{ 'MPS':MPS,  'influencercode':influencercode, 'totalitem':totalitem})
 
class MensWear3(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  MSI = Product.objects.filter(category='MSI')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/MSI.html',{ 'MSI':MSI,  'influencercode':influencercode, 'totalitem':totalitem})

class MensWear4(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  MTT = Product.objects.filter(category='MTT')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/MTT.html',{ 'MTT':MTT,  'influencercode':influencercode, 'totalitem':totalitem})
 







class WoMensWear(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  GTTS = Product.objects.filter(category='GTTS')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/GTTS.html',{ 'GTTS':GTTS,  'influencercode':influencercode, 'totalitem':totalitem})

class WoMensWear1(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  GJP = Product.objects.filter(category='GJP')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/GJP.html',{ 'GJP':GJP,  'influencercode':influencercode, 'totalitem':totalitem})
 
class WoMensWear2(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  GSS = Product.objects.filter(category='GSS')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/GSS.html',{ 'GSS':GSS,  'influencercode':influencercode, 'totalitem':totalitem})
 
class WoMensWear3(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  GSI = Product.objects.filter(category='GSI')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/GSI.html',{ 'GSI':GSI,  'influencercode':influencercode, 'totalitem':totalitem})

class WoMensWear4(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  GS = Product.objects.filter(category='GS')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/GS.html',{ 'GS':GS,  'influencercode':influencercode, 'totalitem':totalitem})
 
class WoMensWear5(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  GTS = Product.objects.filter(category='GTS')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/GTS.html',{ 'GTS':GTS,  'influencercode':influencercode, 'totalitem':totalitem})
 











class boy1(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  b1 = Product.objects.filter(category='b1')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/b1.html',{ 'b1':b1,  'influencercode':influencercode, 'totalitem':totalitem})

class boy2(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  b2 = Product.objects.filter(category='b2')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/b2.html',{ 'b2':b2,  'influencercode':influencercode, 'totalitem':totalitem})
 
class boy3(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  b3 = Product.objects.filter(category='b3')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/b3.html',{ 'b3':b3,  'influencercode':influencercode, 'totalitem':totalitem})
 
class girl1(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  g1 = Product.objects.filter(category='g1')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/g1.html',{ 'g1':g1,  'influencercode':influencercode, 'totalitem':totalitem})
 
class girl2(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  g2 = Product.objects.filter(category='g2')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/g2.html',{ 'g2':g2,  'influencercode':influencercode, 'totalitem':totalitem})
 
class girl3(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  g3 = Product.objects.filter(category='g3')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/g3.html',{ 'g3':g3,  'influencercode':influencercode, 'totalitem':totalitem})
 










class WoMensWear6(View):
 def get(self, request):
  totalitem = 0
  influencercode = request.session.get('influencercode')
#   topwears = Product.objects.filter(category='TW')
  GTT = Product.objects.filter(category='GTT')
#   Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/GTT.html',{ 'GTT':GTT,  'influencercode':influencercode, 'totalitem':totalitem})
 









 

class InfluencerProductView(View):
 def get(self, request):
  totalitem = 0
  user_has_influencer_code = False

    # Logic to check if the user has an influencer code
  if request.user.is_authenticated:
        user_has_influencer_code = bool(request.user.influencercode)
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  Tshirts = Product.objects.filter(category='T')
  if request.user.is_authenticated:
     totalitem = len(InfluencerCart.objects.filter(user=request.user))
  return render(request, 'app/influencerhome.html',{'topwears':topwears, 'bottomwears':bottomwears, 'Tshirts':Tshirts, 'user_has_influencer_code':user_has_influencer_code,  'totalitem':totalitem})
 
@method_decorator(login_required, name='dispatch')
class ProductDetailView(View):
 def get(self, request, pk):
  totalitem = 0
  influencercode = request.session.get('influencercode')
  product = Product.objects.get(pk=pk)
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request,'app/productdetail.html', {'product':product, 'influencercode':influencercode, 'totalitem':totalitem})

class InfluencerProductDetailView(View):
 def get(self, request, pk):
  totalitem = 0
  user_has_influencer_code = False

    # Logic to check if the user has an influencer code
  if request.user.is_authenticated:
        user_has_influencer_code = bool(request.user.influencercode)
  product = Product.objects.get(pk=pk)
  if request.user.is_authenticated:
     totalitem = len(InfluencerCart.objects.filter(user=request.user))
  return render(request,'app/Influencerproductdetail.html', {'product':product, 'user_has_influencer_code':user_has_influencer_code, 'totalitem':totalitem})
 
class Influencer2ProductDetailView(View):
 def get(self, request, pk):
  totalitem = 0
  influencercode = request.session.get('influencercode')
  product = InfluencerCart.objects.get(pk=pk)
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
  return render(request,'app/Influencerproduct2detail.html', {'product':product, 'influencercode':influencercode, 'totalitem':totalitem})
 

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('prod_id')
        size = request.POST.get('size').strip()  # Get the selected size from the form
        color = request.POST.get('color')  # Get the selected color from the form
        print(color)
        print(size)

        # Check if the product with the selected size and color is already in the cart
        if Cart.objects.filter(user=user, product__id=product_id).exists():
            print("Already Exists")
            # Handle the case when the product with the selected size and color is already in the cart
            # messages.warning(request, 'This product is already in your cart.')
        else:
            product = Product.objects.get(id=product_id)
            Cart(user=user, product=product, size=size, color=color).save()
            # Handle the case when the product is added to the cart successfully
            # messages.success(request, 'Product added to cart successfully. Continue your Shopping')

    return redirect('/cart')

@login_required
def buynow(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('prod_id')
        size = request.POST.get('size')  # Get the selected size from the form
        color = request.POST.get('color')  # Get the selected color from the form
        print(color)
        print(size)

        # Check if the product with the selected size and color is already in the cart
        if Cart.objects.filter(user=user, product__id=product_id).exists():
            print("Already Exists")
            messages.warning(request, 'This product is already in your cart. Go to Cart')

            # Handle the case when the product with the selected size and color is already in the cart
            # messages.warning(request, 'This product is already in your cart.')
        else:
            product = Product.objects.get(id=product_id)
            Cart(user=user, product=product, size=size, color=color).save()
            messages.success(request, 'Product added to cart successfully. Continue your Shopping.')

            # Handle the case when the product is added to the cart successfully
            # messages.success(request, 'Product added to cart successfully. Continue your Shopping')

    return redirect('/')
    

@login_required
def show_cart(request):
   totalitem = 0
   influencercode = request.session.get('influencercode')
   if request.user.is_authenticated:
      user = request.user
      cart = Cart.objects.filter(user=user)
      amount = 0.0
      shipping_amount = 0.0
      totalamount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user == user]
      if request.user.is_authenticated:
       totalitem = len(Cart.objects.filter(user=request.user))
      if cart_product:
         for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount
         return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount, 'influencercode':influencercode, 'totalitem':totalitem})
      else:
       return render(request, 'app/emptycart.html', {'totalitem':totalitem, 'influencercode':influencercode})


def plus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity+=1
      c.save()
      amount = 0.0
      shipping_amount = 0.0
      totalamount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
            

      data = {
         'quantity': c.quantity,
         'amount': amount,
         'totalamount': amount + shipping_amount
      }
      return JsonResponse(data)
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        # Ensure the quantity does not go below 1
        if c.quantity > 1:
            c.quantity -= 1
            c.save()

        amount = 0.0
        shipping_amount = 0.0
        totalamount = 0.0
        cart_product = Cart.objects.filter(user=request.user)

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity-=1
      c.delete()
      amount = 0.0
      shipping_amount = 0.0
      totalamount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount 

      data = {
         'amount': amount,
         'totalamount': amount + shipping_amount
      }
      return JsonResponse(data)





def influencercart(request):
 user = request.user
 code = request.user.influencercode
 print(code)
 product_id = request.GET.get('prod_id')
 if InfluencerCart.objects.filter(user=user).count() >= 100:
        print("Maximum quantity reached. Cannot add more products.")
 else:
        # Check if the product is already in the cart
        if InfluencerCart.objects.filter(user=user, product__id=product_id).exists():
            print("Already Exists")
        else:
            product = Product.objects.get(id=product_id)
            InfluencerCart(user=user, product=product, code=code).save()

 return redirect('/influencercart')




def showinfluencercart(request):
   totalitem = 0
   user_has_influencer_code = False

    # Logic to check if the user has an influencer code
   if request.user.is_authenticated:
        user_has_influencer_code = bool(request.user.influencercode)
   if request.user.is_authenticated:
      user = request.user
      influencercart = InfluencerCart.objects.filter(user=user)
      if request.user.is_authenticated:
       totalitem = len(InfluencerCart.objects.filter(user=request.user))
      return render(request, 'app/influencercart.html', {'influencercarts':influencercart, 'user_has_influencer_code':user_has_influencer_code, 'totalitem':totalitem})
   

def influencer_remove_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = InfluencerCart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()
      return redirect('/influencercart')





import razorpay
from django.conf import settings


# stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
 totalitem=0
 influencercode = request.session.get('influencercode')
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 0.0
 totalamount = 0.0
 if request.user.is_authenticated:
       totalitem = len(Cart.objects.filter(user=request.user))

 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
    for p in cart_product:
       tempamount = (p.quantity * p.product.discounted_price)
       amount += tempamount
    totalamount = amount + shipping_amount
 client = razorpay.Client(auth = (settings.KEY, settings.SECRET))
#  key = settings.STRIPE_PUBLISHABLE_KEY
 payment = client.order.create({'amount': totalamount*100.0, 'currency': 'INR', 'payment_capture' : 1})
 print(payment)
#  client = razorpay.Client(auth = (settings.KEY, settings.SECRET))
 return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'influencercode':influencercode, 'totalitem':totalitem, 'payment':payment})



@login_required
def payment_done(request):
   influencercode = request.session.get('influencercode')
   if request.method == 'POST':
      charge = stripe.Charge.create(
         amount = 500,
         currency = 'inr',
         description = 'Payment Gateway',
         source = request.POST['stripeToken']
      )
   user = request.user
   influencer_cart_Products = []
   custid = request.GET.get('custid')
   customer = Customer.objects.get(id=custid)
   cart = Cart.objects.filter(user=user)
   if InfluencerCart.objects.filter(code=influencercode).exists():
      Influencer_product = InfluencerCart.objects.filter(code=influencercode)
      print(Influencer_product)
      for k in Influencer_product:
         influencer_cart_Products.append(k.product)
         print(k.id)
      for c in cart:
            OrderPlaced(
                user=user,
                customer=customer,
                product=c.product,
                quantity=c.quantity,
                size=c.size,
                color=c.color,
                influencercode=influencercode
               #  influencercode=influencercode if c.product in influencer_cart_Products else None
            ).save()
            c.delete()
         
      
   return redirect("orders")

@login_required
def orders(request):
 totalitem=0
 influencercode = request.session.get('influencercode')
 op = OrderPlaced.objects.filter(user=request.user)
 if request.user.is_authenticated:
       totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/orders.html', {'order_placed':op, 'influencercode':influencercode, 'totalitem':totalitem})
 




from django.apps import apps

def loginpage(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            influencercode = form.cleaned_data['influencercode']
            # email = form.cleaned_data['email']

            user = form.get_user()
            a = NewUser.objects.values_list('influencercode')
            #print(a)
            flat_list = [item for tup in a for item in tup]
            #print(flat_list)

            influencer_data = InfluencerCart.objects.filter(code=influencercode)
            # print(influencer_data)
            # #print(influencer_data.user_phonenumber)

            # for users in influencer_data:
            #    username = users.brand
            #    email = users.selling_price

            #    print(email)
            #    print(username)


            if influencercode in  flat_list and influencer_data :
               login(request, user)
               request.session['influencercode'] = influencercode
               return redirect('x_page', influencercode=influencercode)
            #  #influencer=Product.objects.filter(category__in="T-sjhjnirts")
            #  #print(influencer)
            # #  print(influencer.title)
            # #  print(influencer.brand)
            # #  print(influencer.selling_price)
            #  #return render(request, 'app/x.html', {'influencer': influencer})  # Replace 'home' with the URL name of your home page
            #  #return redirect('profile')
            else:
            #     # Handle the case when the influencer code doesn't match any user
                return render(request, 'app/login.html', {'form': form, 'error_message': 'Invalid influencer code'}) 
            # if influencercode in  flat_list:
            #   login(request, user)
            #   return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form}) 

def x_page(request, influencercode):
    totalitem=0
    influencercode = request.session.get('influencercode')
    # Retrieve dynamic data based on influencer code
    influencer_data = InfluencerCart.objects.filter(code=influencercode)
    if request.user.is_authenticated:
       totalitem = len(Cart.objects.filter(user=request.user))
       messages.success(request, f'You have logged in through InfluencerCode: {influencercode}')
      #  messages.success(request, 'You have Logged in through influencerCode : ')


    # Add logic to process the data if needed

    return render(request, 'app/x.html', {'influencer_data': influencer_data, 'influencercode':influencercode, 'totalitem':totalitem})
class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/registration.html', {'form':form})
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   user = form.save(commit=False)
   user.is_active = False
   user.save()

   current_site = get_current_site(request)
   mail_subject = 'Confirm Your Email Address'
   message = render_to_string('app/acc_active_email.html',{
      'user' : user,
      'domain' : current_site.domain,
      'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
      'token' : account_activation_token.make_token(user),
   })
   to_email = form.cleaned_data.get('email')
   email = EmailMessage(
      mail_subject, message, to=[to_email]
   )
   email.send()
  #  form.save()
   messages.success(request, 'Please confirm Your Email Address to complete the registration, Go in your Inbox or check Spam Folder')
   return redirect('registration')
  return render(request, 'app/registration.html', {'form':form})
 

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
   def get(self, request):
      influencercode = request.session.get('influencercode')
      
      form = CustomerProfileForm()
      return render(request, 'app/profile.html', {'form': form, 'influencercode':influencercode, 'active':'btn-primary'})
   
   def post(self, request):
      form = CustomerProfileForm(request.POST)
      if form.is_valid():
         usr = request.user
         name = form.cleaned_data['name']
         locality = form.cleaned_data['locality']
         city = form.cleaned_data['city']
         state = form.cleaned_data['state']
         zipcode = form.cleaned_data['zipcode']
         reg = Customer(user=usr,name=name, locality=locality, city=city, state=state, zipcode=zipcode)
         reg.save()
         messages.success(request, 'Go to Saved Address to select address')
         return redirect('/profile')
      return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})

@login_required
def address(request):
 influencercode = request.session.get('influencercode')
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'influencercode':influencercode, 'active':'btn-primary'})
 #return render(request, 'app/address.html')


# def search(request):
#    totalitem=0
#    influencercode = request.session.get('influencercode')
#    query = request.GET['query']
#    if request.user.is_authenticated:
#        totalitem = len(Cart.objects.filter(user=request.user))
# #    all = Product.objects.filter(title__icontains=query)
#    all = Product.objects.filter(
#     Q(brand__icontains=query) | Q(discounted_price__icontains=query) | Q(title__icontains=query))

#    params = {'all': all, 'influencercode':influencercode, 'totalitem':totalitem}
#    return render(request, 'app/search.html', params)
# #    return HttpResponse("This is search")

from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Product
from .models import Cart

def search(request):
    totalitem = 0
    influencercode = request.session.get('influencercode')

    if 'query' in request.GET and request.GET['query'].strip() != '':
        query = request.GET['query']

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        all = Product.objects.filter(
            Q(brand__icontains=query) | Q(discounted_price__icontains=query) | Q(title__icontains=query)
        )

        params = {'all': all, 'influencercode': influencercode, 'totalitem': totalitem}
        return render(request, 'app/search.html', params)
    else:
        # Redirect to home page if the query is empty
        return redirect('home')  # Replace 'home' with the actual name or URL pattern of your home page

# Make sure to import the necessary modules and models in your views.py file.



def influencer_signup(request):
    if request.method == 'POST':
        form = InfluencerRegistrationForm(request.POST)
        if form.is_valid():
             user = form.save(commit=False)
             user.is_active = False
             user.is_influencer = True
             user.save()
           
             current_site = get_current_site(request)
             mail_subject = 'Confirm Your Email Address'
             message = render_to_string('app/acc_active_email.html',{
                'user' : user,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : account_activation_token.make_token(user),
             })
             to_email = form.cleaned_data.get('email')
             email = EmailMessage(
                mail_subject, message, to=[to_email]
             )
             email.send()
  #  form.save()
             messages.success(request, 'Please confirm Your Email Address to complete the registration, Go in your Inbox or check Spam Folder')
             return redirect('influencersignup')
            # user = form.save(commit=False)
            # user.save()
            # return redirect('getcode')
            #login(request, user)
            #return redirect('home')  # Replace 'home' with the URL name of your home page
    else:
        form = InfluencerRegistrationForm()
    return render(request, 'app/influencersignup.html', {'form': form})


def influencer_login(request):
    if request.method == 'POST':
        form = InfluencerLoginForm(request, request.POST)
        if form.is_valid():
            influencercode = form.cleaned_data['influencercode']
            user_phonenumber = form.cleaned_data['user_phonenumber']
            print(user_phonenumber)

            user = form.get_user()
            if user.influencercode == influencercode and user.user_phonenumber == user_phonenumber:
               login(request, user)
               
               return redirect('influencerhome')  
    else:
        form = InfluencerLoginForm()
    return render(request, 'app/influencerlogin.html', {'form': form})
