from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('productview/<int:myid>', views.productView, name="ProductView"),
    path('checkout/', views.checkout, name="Checkout"),
    path('handlerequest/', views.handlerequest, name='handleRequest'),
    path('login/', views.loginUser, name="loginuser"),
    path('logout/', views.logoutUser, name='logoutuser'),
    path('signin/', views.signinUser, name="signinuser"),
    path('myorders/', views.myorders, name="myorders"),
]
