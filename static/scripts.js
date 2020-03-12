(()=> {

let d = document;
let star1 = d.querySelector('#star1');
let star2 = d.querySelector('#star2');
let star3 = d.querySelector('#star3');
let star4 = d.querySelector('#star4');
let star5 = d.querySelector('#star5');
let user_rating = d.querySelector('#rating')
let user_review = d.querySelector('#review');


document.addEventListener("DOMContentLoaded", function(event){

	d.querySelectorAll('.score').forEach((elem) => {
		elem.addEventListener('click', createRating)
	})
	
	//check to see if review_form exists before adding listener, this prevents console error
	let review_form = d.querySelector('#review_form');
	if(review_form){
		d.querySelector('#review_form').onsubmit = function(e){
				e.preventDefault();
										
				score  = d.querySelector('input[name="score"]:checked').value;
				review = d.querySelector('#review').value;
				
				d.querySelector('#review_form').remove();
				
				var req = new XMLHttpRequest();				
					req.open('POST', d.URL);
					req.onload = function() {			
						console.log(score);
						console.log(review);
					};	
					
					var data = new FormData();
					data.append('score', score);
					data.append('review', review);
					req.send(data);						
		}
	}
  });


function createRating(){
	//console.log(this.value);

	fill  = "&#9733"
	clear = "&#9734"

	if (this.value== '1'){
		star1.innerHTML = fill; 
	    star2.innerHTML = clear;
		star3.innerHTML = clear;
		star4.innerHTML = clear; 
		star5.innerHTML = clear;
		user_rating.innerHTML = star1.title;
	}
	else if (this.value == '2'){
	    star1.innerHTML = fill; 
	    star2.innerHTML = fill;
		star3.innerHTML = clear;
		star4.innerHTML = clear; 
		star5.innerHTML = clear;
		user_rating.innerHTML = star2.title;
	}                                        
	else if (this.value == '3'){            
		star1.innerHTML = fill;
		star2.innerHTML = fill;
		star3.innerHTML = fill;  
        star4.innerHTML = clear;
        star5.innerHTML = clear;
		user_rating.innerHTML = star3.title;
	}                                         
	else if (this.value == '4'){             
		star1.innerHTML = fill;
		star2.innerHTML = fill;
		star3.innerHTML = fill;  
        star4.innerHTML = fill;
        star5.innerHTML = clear;  
		user_rating.innerHTML = star4.title;
	}                                         
	else{                                    
		star1.innerHTML = fill;
		star2.innerHTML = fill;
		star3.innerHTML = fill;
		star4.innerHTML = fill;
		star5.innerHTML = fill;
		user_rating.innerHTML = star5.title;
	} 
} 
 
})();