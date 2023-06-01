from django.db import models

# Create your models here.

class UsersInfo(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100 ,default="null")
    RestaturantName=models.CharField(max_length=100,default="null")
    RestaturantId=models.CharField(max_length=100,default="null")
    
    def __str__(self):
        return self.email

class Restaturant(models.Model):
    choice=(
        ('Restaurant','Restaurant'),
        ('Fast Food','Fast Food'),
        ('Canteen','Canteen'),
    )
    choice1=(
        ('Applied','Applied'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
    )

    RestaturantId=models.CharField(max_length=100)
    RestaturantName=models.CharField(max_length=100)
    RestaturantType=models.CharField(max_length=100,choices=choice)
    email=models.EmailField(max_length=100)
    Ownername=models.CharField(max_length=100,default="null")
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100,default="null")
    city=models.CharField(max_length=100,default="null")
    state=models.CharField(max_length=100,default="null")
    country=models.CharField(max_length=100,default="null")
    pincode=models.CharField(max_length=100,default="null")
    Documents=models.FileField(upload_to='documents/')
    status=models.CharField(max_length=100,choices=choice1,default="null")
    Image=models.FileField(upload_to='RestaurantImages/',default="null")

    def __str__(self):
        return self.RestaturantName+"--"+self.RestaturantId
    
class FoodItem(models.Model):
    choice1=(
        ('Veg','Veg'),
        ('Non-Veg','Non-Veg'),
    )
    choice2=(
        ('Available','Available'),
        ('Not Available','Not Available'),
    )
    choice3=(
        ('Snacks','Snacks'),
        ('Breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner'),
    )

    RestaturantId=models.CharField(max_length=100,default="null")
    ItemId=models.CharField(max_length=100,primary_key=True)
    ItemName=models.CharField(max_length=100)
    Type=models.CharField(max_length=100,choices=choice1)
    Price=models.CharField(max_length=100)
    Category=models.CharField(max_length=100,choices=choice3)
    Description=models.CharField(max_length=1000)
    Status=models.CharField(max_length=100,choices=choice2)
    Image=models.FileField(upload_to='FoodImages/')

    def __str__(self):
        return self.ItemName+"--"+self.ItemId

class Orders(models.Model):

    Choice1=(
        ('Not Paid','Not Paid'),
        ('Paid','Paid'),
    )
    Choice2=(
        ('Ordered','Ordered'),
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
        ('Cooking','Cooking'),
        ('Ready','Ready'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )
    Choice3=(
        ('Home Delivery','Home Delivery'),
        ('Pickup','Pickup'),
        ('Dine In','Dine In'),
    )
    email=models.EmailField(max_length=100)
    OrderId=models.CharField(max_length=100,primary_key=True)
    ItemsInfo=models.CharField(max_length=1000)
    TotalCost=models.CharField(max_length=1000)
    Address=models.CharField(max_length=1000)
    Name=models.CharField(max_length=1000)
    Phone=models.CharField(max_length=1000)
    PaymentStatus=models.CharField(max_length=1000,choices=Choice1)
    Status=models.CharField(max_length=1000,choices=Choice2)
    Date=models.DateField(max_length=1000)
    Time=models.TimeField(max_length=1000)
    OrderType=models.CharField(max_length=1000,choices=Choice3)

    def __str__(self):
        return self.OrderId

class ItemWiseOrders(models.Model):
    OrderId=models.CharField(max_length=100)
    ItemId=models.CharField(max_length=100)
    ItemName=models.CharField(max_length=100)
    Quantity=models.CharField(max_length=100)
    Price=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    RestaturantId=models.CharField(max_length=100,default="null")

    def __str__(self):
        return self.OrderId+"--"+self.ItemName

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    Subject=models.CharField(max_length=100)
    message=models.CharField(max_length=1000)

    def __str__(self):
        return self.Subject