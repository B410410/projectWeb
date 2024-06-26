"""
URL configuration for projectWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Web_MSI import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('index2/', views.index2),
    path('story/', views.story),
    path('story2/', views.story2),
    path('login/', views.memberlogin),
    path('logout/', views.memberlogout),
    path('register/', views.sign_up, name='register'),
    path('shop/', views.shop),
    path('shop2/', views.shop2),
    path('detail/<int:productid>/', views.detail),
    path('detail2/<int:productid>/', views.detail2),
    path('addtocart/<str:ctype>/', views.addtocart),
    path('addtocart/<str:ctype>/<int:productid>/', views.addtocart),
    path('cart/', views.cart),
    path('cartorder/', views.cartorder),
    path('cartok/', views.cartok),
    path('cartordercheck/', views.cartordercheck),
]
