import json
from .models import *

def cookieBasket(request):

	#Create empty basket for now for non-logged in user
	try:
		basket = json.loads(request.COOKIES['basket'])
	except:
		basket = {}
		print('BASKET:', basket)

	items = []
	order = {'get_basket_total':0, 'get_basket_items':0, 'shipping':False}
	basketItems = order['get_basket_items']

	for i in basket:
		#We use try block to prevent items in basket that may have been removed from causing error
		try:
			basketItems += basket[i]['quantity']

			product = Product.objects.get(id=i)
			total = (product.price * basket[i]['quantity'])

			order['get_basket_total'] += total
			order['get_basket_items'] += basket[i]['quantity']

			item = {
				'id':product.id,
				'product':{'id':product.id,'name':product.name, 'price':product.price, 
				'imageURL':product.imageURL}, 'quantity':basket[i]['quantity'],
				'digital':product.digital,'get_total':total,
				}
			items.append(item)

			if product.digital == False:
				order['shipping'] = True
		except:
			pass
			
	return {'basketItems':basketItems ,'order':order, 'items':items}

def basketData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		basketItems = order.get_basket_items
	else:
		cookieData = cookieBasket(request)
		basketItems = cookieData['basketItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'basketItems':basketItems ,'order':order, 'items':items}

	
def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieBasket(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
		)
	customer.name = name
	customer.save()

	order = Order.objects.create(
            customer=customer,
            complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
		)
	return customer, order