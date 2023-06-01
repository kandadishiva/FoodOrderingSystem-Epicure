from django.urls import path
from EpicureApp import views


urlpatterns = [
    path('',views.index,name="index"),
    path('aboutus',views.aboutus,name="aboutus"),
    path('contact',views.contact,name="contact"),
    path('home',views.home,name="home"),
    path('newrestaurant',views.newrestaurant,name="newrestaurant"),
    path('RestaurantStatus',views.RestaurantStatus,name="RestaurantStatus"),
    path('AddFood',views.AddFood,name="AddFood"),
    path('BillingPage',views.BillingPage,name="BillingPage"),
    path('handlerequest',views.handlerequest,name="handlerequest"),
    path('MyOrders',views.MyOrders,name="MyOrders"),
    path('CancelOrder/<str:orderid>',views.CancelOrder,name="CancelOrder"),
    path('ViewOrder/<str:orderid>',views.ViewOrder,name="ViewOrder"),
    path('FoodItems/<str:RestaturantId>',views.FoodItems,name="FoodItems"),
    path('RestaturantFoodItems',views.RestaturantFoodItems,name="RestaturantFoodItems"),
    path('CustomerOrders',views.CustomerOrders,name="CustomerOrders"),
    path('CustomerViewOrder/<str:orderid>',views.CustomerViewOrder,name="CustomerViewOrder"),
]