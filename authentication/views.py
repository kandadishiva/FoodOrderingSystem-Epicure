from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .utils import TokenGenerator,generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from EpicureApp.models import UsersInfo
from EpicureApp.models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.

def signup(request):
    #food Items from database to display in index page category wise
    allitems=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(Status="Available")
    Breakfast=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(Status="Available",Category="Breakfast")
    Lunch=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(Status="Available",Category="Lunch")
    Dinner=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(Status="Available",Category="Dinner")
    Snacks=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(Status="Available",Category="Snacks")

    #Restaturant from database to display in index page
    Restaturants=Restaturant.objects.values('RestaturantId','RestaturantName','RestaturantType','Documents','RestaturantId','Image','address').filter(status="Approved",RestaturantType="Restaurant")
    Canteens=Restaturant.objects.values('RestaturantId','RestaturantName','RestaturantType','Documents','RestaturantId','Image','address').filter(status="Approved",RestaturantType="Canteen")
    FastFood=Restaturant.objects.values('RestaturantId','RestaturantName','RestaturantType','Documents','RestaturantId','Image','address').filter(status="Approved",RestaturantType="Fast Food")

    #Count of no fo food items and Restaurants
    ItemsCount=FoodItem.objects.all().count()
    RestaturantCount=Restaturant.objects.all().count()
    ordercount=Orders.objects.all().count()
    DeliveredCount=Orders.objects.filter(Status="Delivered").count()

    Count={"ItemsCount":ItemsCount,"RestaturantCount":RestaturantCount,"ordercount":ordercount,"DeliveredCount":DeliveredCount}

    con={"AllItems":allitems,"BreakfastItems":Breakfast,"LunchItems":Lunch,"DinnerItems":Dinner,"SnacksItems":Snacks,"Count":Count,"Restaturants":Restaturants,"Canteens":Canteens,"FastFood":FastFood}

    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        name=request.POST['name']
        if password!=confirm_password:
            messages.warning(request,"Password and Confirm Password are not same")
            return render(request,"signup.html",con)
        try:
            if User.objects.get(username=email):
                messages.warning(request,"User already exists")
                return render(request,"signup.html",con)
            
        except Exception as identifier:
            pass

        info=UsersInfo(name=name,email=email)
        info.save()

        user=User.objects.create_user(email,email,password)
        user.is_active=False
        user.save()

        email_subject="Activate your account"
        message=render_to_string("activate.html",{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })

        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        email_message.send()

        messages.success(request,"Activation link has been sent to your email address")
        return render(request,"login.html",con)
    return render(request,"signup.html",con)

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account activated successfully")
            return render(request,"login.html")
        return render(request,"activatefail.html")
def login(request):
    #food Items from database to display in index page category wise
    allitems=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(Status="Available")
    Breakfast=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(Status="Available",Category="Breakfast")
    Lunch=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(Status="Available",Category="Lunch")
    Dinner=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(Status="Available",Category="Dinner")
    Snacks=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(Status="Available",Category="Snacks")

    #Restaturant from database to display in index page
    Restaturants=Restaturant.objects.values('RestaturantId','RestaturantName','RestaturantType','Documents','RestaturantId','Image','address').filter(status="Approved",RestaturantType="Restaurant")
    Canteens=Restaturant.objects.values('RestaturantId','RestaturantName','RestaturantType','Documents','RestaturantId','Image','address').filter(status="Approved",RestaturantType="Canteen")
    FastFood=Restaturant.objects.values('RestaturantId','RestaturantName','RestaturantType','Documents','RestaturantId','Image','address').filter(status="Approved",RestaturantType="Fast Food")

    #Count of no fo food items and Restaurants
    ItemsCount=FoodItem.objects.all().count()
    RestaturantCount=Restaturant.objects.all().count()
    ordercount=Orders.objects.all().count()
    DeliveredCount=Orders.objects.filter(Status="Delivered").count()

    Count={"ItemsCount":ItemsCount,"RestaturantCount":RestaturantCount,"ordercount":ordercount,"DeliveredCount":DeliveredCount}

    con={"AllItems":allitems,"BreakfastItems":Breakfast,"LunchItems":Lunch,"DinnerItems":Dinner,"SnacksItems":Snacks,"Count":Count,"Restaturants":Restaturants,"Canteens":Canteens,"FastFood":FastFood}

    if request.method=="POST":
        email=request.POST["email"]
        pwd=request.POST["pass"]
        user=authenticate(username=email,password=pwd)

        if user is not None:
            auth_login(request,user)
            return redirect('/home')
        else:
            user=None
            messages.warning(request,"Invalid Username or Password")
            return render(request,"login.html",con)
    return render(request,"login.html",con)

def logout(request):
    auth_logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('/validate/login')

class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            # current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()

            messages.success(request,"We have sent you an email with instructions on how to reset your password")

            return render(request,'request-reset-email.html')

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'set-new-password.html',context)
        
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success Please Login with NewPassword")
            return redirect('/validate/login/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'set-new-password.html',context)

        return render(request,'set-new-password.html',context)