window.onload = function () {
					pswd_retype_box = document.getElementById("id_passwd_check");
					pswd_retype_box.style.backgroundColor = "#8591AB";
					
				
					check_box = document.getElementById("chk");
					check_box.onclick= function(){
								if(check_box.checked)
								{
									pswd_retype_box.style.backgroundColor = "#FFFFFF";
									pswd_retype_box.removeAttribute("disabled");
								}
								else
								{
									pswd_retype_box.style.backgroundColor = "#8591AB";
									pswd_retype_box.setAttribute("disabled","disabled");
								}
					};
					
					f = document.getElementById("login");
					f.onsubmit = function(){
							usr = document.getElementById("id_username");
							passwd = document.getElementById("id_password");
							
							err = "";
							
							if(usr.value.length === 0 || usr.value.length >30){
								err+="<li>Enter an username with characters less than 30 characters</li>";
							}
							if(passwd.value.length === 0){
								err +="<li>Enter a password</li>";
							}
							else if(check_box.checked && passwd.value !== pswd_retype_box.value){
								err +="<li>Passwords do not match in the given boxes</li>";
							}								
								
							if( err !== "")
							{
								e = document.getElementById("errors");
								e.innerHTML="<ul>"+err+"</ul>";
								return false;
							}
					};
	}
