from django.contrib.auth.decorators import login_required
from .utils import cookieBasket, basketData, guestOrder
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import UserRegisterForm
from .models import * 
import datetime
import json



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'store/profile.html')


def store(request):
	data = basketData(request)

	basketItems = data['basketItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {
		'products': products, 
		'basketItems': basketItems,
	}
	return render(request, 'store/store.html', context)


def basket(request):
	data = basketData(request)

	basketItems = data['basketItems']
	order = data['order']
	items = data['items']

	context = {
		'items': items, 
		'order': order, 
		'basketItems': basketItems,
	}
	return render(request, 'store/basket.html', context)


def checkout(request):
	data = basketData(request)
	
	basketItems = data['basketItems']
	order = data['order']
	items = data['items']

	context = {
		'items': items, 
		'order': order, 
		'basketItems': basketItems,
	}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

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

	if total == order.get_basket_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)