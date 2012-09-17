
window.onload = function () {
	
	var title = document.getElementById('id_title');
	var slug = document.getElementById('id_slug');
	var raw_ct = document.getElementById('id_raw_content');
	
	//~ slug.style.backgroundColor="red"
	
	function insertAfter (ref,new_node) {
		ref.parentNode.insertBefore(new_node,ref.nextSibiling);
	} 
	function insertError(element,message) {
		var x = document.createElement("td");
		arr.push(x);
		x.className="custom_err";
		x.innerHTML = message;
		x.style.color = "red";
		insertAfter(element,x);
	}
	
	f = document.getElementById("edit_form");
	arr = [];
	f.onsubmit = function () {
		for(var i=0;i<arr.length;++i) {
			arr[i].parentNode.removeChild(arr[i]);
		}
		arr=[];
		e_count = 0;
		if(title.value.length === 0) {
			insertError(title,"Please enter a title");
			e_count++;
		}
		if(slug.value.length === 0) {
			insertError(slug,'Please enter a unique slug');
			e_count++;
		}
		if(raw_ct.value.length === 0) {
			insertError(raw_ct,'Please enter a content');
			e_count++;
		}
		if(e_count > 0){
			return false;
		}
	}
	
}
	
