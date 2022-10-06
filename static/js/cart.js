let previous_value;

document.getElementById("inp").addEventListener("change", function() {
  let value = document.getElementById("inp").value;
  if (previous_value > value) {
    console.log("Decreased");
  } else if (previous_value < value) {
    console.log("Increased");
  }
  previous_value = value;
});

var updateBtns = document.getElementsByClassName("add-to-cart")
for(var i = 0; i < updateBtns.length; i++){
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('product : ',productId, 'action : ',action)
		console.log('USER:', user)
		if(user === 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}




function addCookieItem(productId, action){
	console.log('User is not authenticated')
		if (action == 'add'){
			if(cart[productId] == undefined){
			cart[productId] = {'quantity':1} 
			}else{
				cart[productId]['quantity'] +=1
			}
		}
		if(action == 'remove'){
			cart[productId]['quantity'] -=1
			if(cart[productId]['quantity'] <=0){
				console.log('remove item')
				delete cart[productId]
			}
		}
		console.log('cart:', cart)
		document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
		self.location.reload();




	}

function updateUserOrder(productId, action){
	console.log('User is logged in ')
	var url = '/update_item/'
	fetch(url, {
		method: 'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken,
		},
		body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) =>{
			return response.json()
		})
		.then((data)=>{
			console.log('data:', data);
            self.location.reload();
		})
}


