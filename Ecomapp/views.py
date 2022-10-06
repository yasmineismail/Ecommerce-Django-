from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import *
import datetime
from .forms import *
from . utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_protect

def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name='customer')
			user.groups.add(group)
			Customer.objects.create(
				user=user,
				name=user.username,
				email=user.email,
				)
			messages.success(request, 'Account was created for ' +username)
			return redirect('login')
	context = {'form' :form}
	return render(request, 'store/reg.html',context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('store')
		else:
			messages.info(request, 'username or password is incorrect')
	context = {}
	return render(request, 'store/Login.html', context)

def store(request):
	data = cartData(request)
	carItems = data['carItems']
	order = data['order']
	items = data['items']  
	products = Product.objects.all()
	context = {'products': products,'carItems':carItems,'items':items, 'order':order,}
	return render(request, 'store/store.html', context)

def cart(request):
	data = cartData(request)
	carItems = data['carItems']
	order = data['order']
	items = data['items']  		
	context = {'items':items, 'order':order, 'carItems':carItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	carItems = data['carItems']
	order = data['order']
	items = data['items'] 
	context = {'items':items, 'order':order, 'carItems':carItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('action:', action)
	print('productId:', productId)
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was added', safe=False)

@csrf_protect
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)
	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	if total == order.get_cart_total:
		order.complete = True
	order.save()
	if order.shipping == True:
		ShippingAdress.objects.create(
			customer=customer,
			order=order,
			adress=data['form']['adress'],
			city=data['form']['city'],
			state=data['form']['state'],
			zipcode=data['form']['zipcode'],
		)
	return JsonResponse('Payment subbmitted..',safe=False) 







