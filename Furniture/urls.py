"""
URL configuration for Furniture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from myApp import views
from django.conf import settings
from django.contrib.staticfiles.urls import static 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns =[
    path("admin/", admin.site.urls),
    path("footer2", views.footer2),
    
    path("sample", views.sample),
    path("register", views.register),
    path("", views.login, name='login'),
    path("profile", views.userprofile),
    path("Allproducts", views.Allproducts, name="Allproducts"),
    path("filterproducts/<str:name>", views.filterproducts, name='filterproducts'),
    path("detail/<int:id>", views.detail ,name="detailproduct"),
    path("add_to_cart", views.add_to_cart ,name="add_to_cart"),
    path("show_add_to_cart", views.show_add_to_cart ,name="show_add_to_cart"),
    path('increment/<int:item_id>', views.increment_quantity, name='increment_quantity'),
    path('decrement/<int:item_id>',  views.decrement_quantity, name='decrement_quantity'),
    path('remove/<int:item_id>/', views.remove_item, name='remove_item'),  # URL for removing item
    # path('cart/', views.cart_detail, name='cart_detail'),  # Your cart detail page
    path('clear/',views.clear_cart, name='clear_cart'),
    path('create-order/' ,views.create_order, name='create_order' ),
    path('save_payment/', views.save_payment, name='save_payment'),
    path('shipping_address_view', views.shipping_address_view,name='shipping_address_view'),
    path('check_out', views.check_out,name='checkout'),
    path('success_page', views.success_page,name='success'),
    path('myorder/', views.my_orders, name='my_orders'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('home_page/', views.home_page, name='home_page'),
    
]
urlpatterns+= staticfiles_urlpatterns()
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

