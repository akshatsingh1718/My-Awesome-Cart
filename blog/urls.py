from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="blogPage"),
    path('blogpost/<int:blogId>', views.blogPost, name="blogPost"),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('contact/', views.contactUs, name='contactus'),
    path('login/', views.loginUser, name="loginuser"),
    path('logout/', views.logoutUser, name='logoutUSer'),
    # API to post comment
    path('blogpostcomment/', views.blogpostComment, name="blogpostComment"),
    path('createblog/', views.createBlog, name='createBlog'),
    path('mycreations/', views.myCreations, name='myCreations'),
]
