from django.shortcuts import render,redirect
from EpicureApp.models import Contact
from django.contrib.auth.models import User
from EpicureApp.models import *
from django.contrib import messages
import json
import random
from EpicureApp import keys
from django.conf import settings
MERCHANT_KEY=keys.MK
from django.views.decorators.csrf import  csrf_exempt
from PayTm import Checksum
import datetime
# Create your views here.

def index(request):
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

    #Restaturant Status

    Count={"ItemsCount":ItemsCount,"RestaturantCount":RestaturantCount,"ordercount":ordercount,"DeliveredCount":DeliveredCount}

    con={"AllItems":allitems,"BreakfastItems":Breakfast,"LunchItems":Lunch,"DinnerItems":Dinner,"SnacksItems":Snacks,"Count":Count,"Restaturants":Restaturants,"Canteens":Canteens,"FastFood":FastFood}

    return render(request,"index.html",con)

def home(request):
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

    #Restaturant Status
    username=request.user.username
    res=Restaturant.objects.filter(email=username,status="Approved")

    if len(res)==0:
        status="Not Approved"
    else:
        status="Approved"

    con={"AllItems":allitems,"BreakfastItems":Breakfast,"LunchItems":Lunch,"DinnerItems":Dinner,"SnacksItems":Snacks,"Count":Count,"Restaturants":Restaturants,"Canteens":Canteens,"FastFood":FastFood,"status":status}
    return render(request,"home.html",con)

def newrestaurant(request):
    if request.method=="POST":
        rname=request.POST["name"]
        rtype=request.POST["Rtype"]
        raddress=request.POST["address"]
        Ownername=request.POST["ownername"]
        ownerno=request.POST["ownerno"]
        doc=request.FILES["file1"]
        img=request.FILES["file2"]
        email=request.user.username

        if (ownerno.isdigit()==False or len(ownerno)!=10):
            messages.warning(request,"Invalid Phone Number")
            return render(request,"newrestaurant.html")

        rid="R"+str(len(Restaturant.objects.all())+1)
        res=Restaturant(RestaturantId=rid,RestaturantName=rname,RestaturantType=rtype,address=raddress,phone=ownerno,email=email,Documents=doc,Ownername=Ownername,status="Applied",Image=img)
        res.save()

        UsersInfo.objects.filter(email=email).update(RestaturantId=rid,RestaturantName=rname)
        return redirect("/RestaurantStatus")
    else:
        username=request.user.username
        res=Restaturant.objects.filter(email=username)
        if len(res)==0:
            return render(request,"newrestaurant.html")
        else:
            return redirect("/RestaurantStatus")

    return render(request,"newrestaurant.html")

def RestaurantStatus(request):
    username=request.user.username
    res=Restaturant.objects.filter(email=username)
    status=res[0].status
    con={"status":status}
    return render(request,"RestaurantStatus.html",con)\
    
def FoodItems(request,RestaturantId):
    items=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(RestaturantId=RestaturantId)
    RestaturantInfo=Restaturant.objects.values('RestaturantName','RestaturantType','address','phone','email','Documents','Ownername','Image','RestaturantId').filter(RestaturantId=RestaturantId)
    con={"items":items,"RestaturantInfo":RestaturantInfo[0]}
    return render(request,"FoodItems.html",con)

def RestaturantFoodItems(request):
    username=request.user.username
    RestaturantId=Restaturant.objects.filter(email=username)[0].RestaturantId
    items=FoodItem.objects.values('ItemName','Price','Image','Description','ItemId').filter(RestaturantId=RestaturantId)
    RestaturantInfo=Restaturant.objects.values('RestaturantName','RestaturantType','address','phone','email','Documents','Ownername','Image','RestaturantId').filter(RestaturantId=RestaturantId)
    con={"items":items,"RestaturantInfo":RestaturantInfo[0]}
    return render(request,"RestaturantFoodItems.html",con)

def AddFood(request):
    if request.method=="POST":
        FoodName=request.POST["name"]
        FoodType=request.POST["Ftype"]
        FoodPrice=request.POST["price"]
        FoodStatus="Available"
        FoodCategory=request.POST["FCategory"]
        FoodImage=request.FILES["image"]
        Description=request.POST["description"]

        username=request.user.username
        RId=Restaturant.objects.filter(email=username)[0].RestaturantId
        RestaturantId=RId
        print(RestaturantId)
        ItemId="I"+str(len(FoodItem.objects.all())+1)+"--"+RestaturantId
        res=FoodItem(ItemId=ItemId,ItemName=FoodName,RestaturantId=RestaturantId,Type=FoodType,Price=FoodPrice,Status=FoodStatus,Category=FoodCategory,Image=FoodImage,Description=Description)
        res.save()
        mesg=FoodName+" is added to your menu successfully!!"
        messages.success(request,mesg)
        return render(request,"AddFood.html")
    return render(request,"AddFood.html")

def BillingPage(request):

    username=request.user.username
    ans=UsersInfo.objects.filter(email=username)
    name=ans[0].name
    phno=ans[0].phone
    con={"name":name,"phno":phno,"email":username}
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/validate/login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name=request.POST.get('name','')
        address=request.POST.get('address','')
        phno=request.POST.get('phno','')
        items = items_json.replace('\n', '').replace('  ', '')
        items = json.loads(items)
        ordertype="Home Delivery"
        OrderStatus="Ordered"
        PaymentStatus="Paid"
        username=request.user.username
        amount=request.POST.get('amt','')
        if (phno.isdigit()==False or len(phno)!=10):
            messages.warning(request,"Invalid Phone Number")
            return render(request,"BillingPage.html",con)
        if (amount=="0"):
            messages.warning(request,"Please Select Items to Order your cart is empty")
            return render(request,"BillingPage.html",con)
        while True:
            orderid=random.randint(100000,999999)
            try:
                a=Orders.objects.get(OrderId=orderid)
            except:
                break
        date=datetime.datetime.now().strftime("%Y-%m-%d")
        time=datetime.datetime.now().strftime("%H:%M:%S")

        order=Orders(OrderId=orderid,email=username,OrderType=ordertype,Status=OrderStatus,PaymentStatus=PaymentStatus,ItemsInfo=items,Name=name,Address=address,TotalCost=amount,Phone=phno,Date=date,Time=time)
        order.save()

        for i in items:
            id=i.replace("pr","")
            rid=id.split("--")[1]
            Name=FoodItem.objects.filter(ItemId=id)[0].ItemName
            Price=FoodItem.objects.filter(ItemId=id)[0].Price
            Quantity=items[i][0]
            OrderId=orderid
            ItemWiseOrders(OrderId=OrderId,ItemId=id,ItemName=Name,Price=Price,Quantity=Quantity,RestaturantId=rid,email=username).save()

        messages.success(request,"Order Placed Successfully!!")

        thank = True
# # PAYMENT INTEGRATION

        id = orderid
        oid=str(id)+"Epicure"
        param_dict = {

            'MID':keys.MID,
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': username,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        con["param_dict"]=param_dict
        return render(request, 'paytm.html',con)
        
    return render(request,"BillingPage.html",con)

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            a=response_dict['ORDERID']
            b=response_dict['TXNAMOUNT']
            rid=a.replace("Epicure","")
           
            print(rid)
            filter2= Orders.objects.filter(OrderId=rid)
            print(filter2)
            print(a,b)
            for post1 in filter2:

                #post1.oid=a
                #post1.amountpaid=b
                post1.PaymentStatus="Paid"
                post1.save()
            print("run agede function")
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

def MyOrders(request):
    username=request.user.username
    orders=Orders.objects.values('OrderId','ItemsInfo','TotalCost','Date','Time','Status','PaymentStatus',"OrderType").filter(email=username)
    for i in orders:
        length=len(i["ItemsInfo"].split(":"))
        i['ItemsInfo']=length//2
    order1=Orders.objects.values('OrderId','ItemsInfo','TotalCost','Date','Time','Status','PaymentStatus',"OrderType").filter(email=username,Status="Delivered")
    for i in order1:
        length=len(i["ItemsInfo"].split(":"))
        i['ItemsInfo']=length//2
    orders2=Orders.objects.values('OrderId','ItemsInfo','TotalCost','Date','Time','Status','PaymentStatus',"OrderType").filter(email=username,Status="Cancelled")
    for i in orders2:
        length=len(i["ItemsInfo"].split(":"))
        i['ItemsInfo']=length//2
        
    con={"orders":orders,"CompletedOrders":order1,"CancelledOrders":orders2}
    return render(request,"Orders.html",con)

def CustomerOrders(request):
    username=request.user.username
    RestaturantId=Restaturant.objects.values('RestaturantId').filter(email=username)[0]["RestaturantId"]
    orders=ItemWiseOrders.objects.values('OrderId','ItemId','ItemName','Price','Quantity','email').filter(RestaturantId=RestaturantId)
    allorders={}
    for i in orders:
        if i["OrderId"] not in allorders:
            allorders[i["OrderId"]]=[]
        allorders[i["OrderId"]].append(i)
 
    currentorders=[]
    cancelledorders=[]
    completedorders=[]
    for i in allorders:
        orders=Orders.objects.values('OrderId','ItemsInfo','TotalCost','Date','Time','Status','PaymentStatus',"OrderType").filter(OrderId=i)
        k=orders[0]
        k["ItemsInfo"]=len(allorders[i])

        if orders[0]["Status"]=="Delivered":
            completedorders.append(k)
        elif orders[0]["Status"]=="Cancelled":
            cancelledorders.append(k)
        else:
            currentorders.append(k)
    con={"orders":currentorders,"CompletedOrders":completedorders,"CompletedOrders":cancelledorders,"status":"Approved"}
    return render(request,"Orders.html",con)

def CancelOrder(request,orderid):
    username=request.user.username
    Orders.objects.filter(OrderId=orderid).update(Status="Cancelled")

    messages.success(request,"Order Cancelled Successfully!!")
    return redirect("/MyOrders")

def ViewOrder(request,orderid):
    username=request.user.username
    orders=Orders.objects.values('OrderId','ItemsInfo','TotalCost','Date','Time','Status','PaymentStatus',"OrderType","Name","Address","Phone").filter(email=username,OrderId=orderid)
    a=eval(orders[0]["ItemsInfo"])
    z=[]
    totalcost=0
    for i in a:
        id=i.replace("pr","")
        f=FoodItem.objects.values('ItemName','Price','Image').filter(ItemId=id)
        k=f[0]
        k["Quantity"]=a[i][0]
        z.append(k)
        totalcost+=int(k["Price"])*int(a[i][0])
    con={"Items":z,"orderid":orderid,"TotalCost":totalcost,"Date":orders[0]["Date"],"Time":orders[0]["Time"],"Status":orders[0]["Status"],"PaymentStatus":orders[0]["PaymentStatus"],"OrderType":orders[0]["OrderType"]}

    return render(request,"ViewOrder.html",con)

def CustomerViewOrder(request,orderid):
    if request.method=="POST":
        status=request.POST.get("Rtype","")
        Orders.objects.filter(OrderId=orderid).update(Status=status)
        messages.success(request,"Order Status Updated Successfully!!")
    username=request.user.username
    RestaturantId=Restaturant.objects.values('RestaturantId').filter(email=username)[0]["RestaturantId"]
    Items=ItemWiseOrders.objects.values('ItemId','ItemName','Price','Quantity','email').filter(RestaturantId=RestaturantId,OrderId=orderid)
    Orderstatus=Orders.objects.values('Status').filter(OrderId=orderid)[0]["Status"]
    z=[]
    for i in Items:
        id=i["ItemId"]
        f=FoodItem.objects.values('ItemName','Price','Image').filter(ItemId=id)
        k=f[0]
        k["Quantity"]=i["Quantity"]
        z.append(k)

    con={"Items":z,"orderid":orderid,"OrderStatus":Orderstatus,"Status":"Approved"}
    return render(request,"ViewOrder.html",con)

def aboutus(request):
    return render(request,"aboutus.html")

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        Subject=request.POST.get('subject')
        message=request.POST.get('message')
        con=Contact(name=name,email=email,Subject=Subject,message=message)
        con.save()
        return render(request,"login.html")
    return render(request,"index.html")