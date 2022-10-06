
from django.urls import path

from . import views

from django.urls import path
from . import views 

urlpatterns = [
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('login/', views.loginPage, name="login"),
	path('reg/', views.registerPage, name="reg")


]