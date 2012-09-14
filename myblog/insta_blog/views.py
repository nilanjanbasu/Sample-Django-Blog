# Create your views here.

from django.shortcuts import render_to_response
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.template import RequestContext
from django.forms import ModelForm
from insta_blog.models import Article
from django.contrib.auth.models import User

class LoginForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')

	def save(self, commit=True):
		usr = super(LoginForm, self).save(commit=False)
		usr.set_password(self.cleaned_data["password"])
		if commit:
			usr.save()
		return usr

def register_new_account(request,template_file_name):
	
	logout(request)
	
	f = LoginForm(request.POST)
	if f.is_valid():
			f.save()			
			return HttpResponseRedirect('/registered/')
	
	return render_to_response(template_file_name,{ 'error_message': f.errors.values, 'u_name':'','pswd':''},context_instance=RequestContext(request))
	

def login_serve(request):		
	
	username=''
	password=''
	error_message = ''
	if request.method == 'GET':
		logout(request)
		
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		if "create_new" in request.POST.keys():
			return register_new_account(request,'login_template.html')		
		
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return HttpResponseRedirect('/logged_in/') #TODO Replace by something real!
		else:
			error_message = "Username-password does not match"
			
	return render_to_response('login_template.html',{ 'error_message': [error_message,], 'u_name':username,'pswd':''},context_instance=RequestContext(request))

def logged_in_message(request):
	name = 'Unknown User'
	if request.user.is_authenticated():
		name = request.user.username
	
	return HttpResponse("Hello,%s"%(name,))

def foo():
	pass
	

def view_all_articles_by_user(request,blog_name,page_number=1):
	
	pg = (int(page_number)-1)*10
	try:
		usr = User.objects.get(username=blog_name)
	except User.DoesNotExist:
		raise Http404
	
	articles = usr.article_set.all()[pg:pg+10]
	if len(articles) == 0:
		raise Http404	
	else:
		return render_to_response('view_blog_template.html',{'articles':articles,'username':blog_name},context_instance=RequestContext(request))
	
	
def view_particular_blogpage(request,blog_name,pg_name):
	
	try:
		#~ usr = User.objects.get(username=blog_name)		
		#~ print usr.article_set.all()
		#~ art = usr.article_set.filter(slug=pg_name)
		
		art = Article.author_objects.user_articles(blog_name).filter(slug=pg_name)
		if len(art) == 0 :
			raise Http404	
		return render_to_response('individual_article_template.html',{'p':art[0]},context_instance=RequestContext(request))
				
	except User.DoesNotExist:
		raise Http404
	
	
	
	
