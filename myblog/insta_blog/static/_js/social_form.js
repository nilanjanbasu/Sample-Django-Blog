window.onload = function () {	
	var f = document.getElementById('id_social_form');
	arr = [];
	f.onsubmit = function () {
		if(arr.length > 0 ) {
			f.parentNode.parentNode.removeChild(arr[0]);
		}
		arr = [];
		var txtbx = document.getElementById('id_username');
		if(txtbx.value.length == 0 || txtbx.value.length >30) {
			var x = document.createElement("p");
			arr.push(x);
			x.innerHTML='Enter valid username less than 30 characters';
			x.style.backgroundColor = "white";
			f.parentNode.parentNode.insertBefore(x,f.parentNode);
			return false;
		}
	};
};
