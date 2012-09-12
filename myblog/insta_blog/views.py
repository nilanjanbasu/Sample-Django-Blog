# Create your views here.

import myblog.insta_blog.forms.login as login_form
from django.shortcuts import render_to_response
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext

def login_serve(request):
	f = login_form.LoginForm()
	
	if request.method == 'GET':
		if request.user.is_authenticated():
			logout(request)
		
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return HttpResponseRedirect('/logged_in/') #TODO Replace by something real!
			
	return render_to_response('login_template.html',{ 'login_form': f},context_instance=RequestContext(request))

def logged_in_message(request):
	name = 'Unknown User'
	if request.user.is_authenticated():
		name = request.user.username
	
	return HttpResponse("Hello,%s"%(name,))
