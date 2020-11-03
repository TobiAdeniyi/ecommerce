var updateBtns = document.getElementsByClassName('update-basket')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (basket[productId] == undefined){
		basket[productId] = {'quantity':1}

		}else{
			basket[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		basket[productId]['quantity'] -= 1

		if (basket[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete basket[productId];
		}
	}
	console.log('BASKET:', basket)
	document.cookie ='basket=' + JSON.stringify(basket) + ";domain=;path=/"
	
	location.reload()
}