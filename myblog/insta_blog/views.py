# Create your views here.

from django.shortcuts import render_to_response
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.template import RequestContext
from django.forms import ModelForm
from insta_blog.models import Article
from django.contrib.auth.models import User
from django.db import models
from insta_blog.blog_forms import ArticleForm
from datetime import datetime

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

class NavBarLinks(object):
	def __init__(self,text,view_name,param_dict=dict(),query_string=''):
		self.text = text
		self.view_name = view_name
		self.paramdict = param_dict
		self.query_string = query_string
		
	@models.permalink
	def get_absolute_url(self):
		return (self.view_name,(),self.paramdict)
		
	def get_url_with_query_info(self):
		return (self.get_absolute_url()+self.query_string)
		
def register_new_account(request,template_file_name):
	
	logout(request)
	
	f = LoginForm(request.POST)
	if f.is_valid():
		f.save()
		usr = authenticate(username=f.cleaned_data['username'],password=f.cleaned_data['password'])
		login(request,usr)				
		return HttpResponseRedirect('/user/%s/'%(f.cleaned_data['username'],))
	
	return render_to_response(template_file_name,{ 'error_message': f.errors.values, 'u_name':'','pswd':''},context_instance=RequestContext(request))
	
def log_out_serve(request):
	referrer = request.META.get('HTTP_REFERER',None)	
	print referrer
	logout(request)
	if referrer is None:
		return HttpResponseRedirect('/login/')
	else:
		return HttpResponseRedirect(referrer)

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
			if 'next' in request.GET:
				return HttpResponseRedirect(request.GET['next'])
			else:
				return HttpResponseRedirect('/user/%s/'%(username,)) #TODO Replace by something real!
		else:
			error_message = "Username-password does not match"
			
	return render_to_response('login_template.html',{ 'error_message': [error_message,], 'u_name':username,'pswd':''},context_instance=RequestContext(request))


def render_with_navlist(request,template_name,var_dict,context_instance):
	
	links_list = []
	if request.user.is_authenticated():
		links_list.append(NavBarLinks('Profile','profile_view',{'user_name':request.user.username}))
		links_list.append(NavBarLinks('Log Out','logout_page')) ############################### FILL UP
	else:
		links_list.append(NavBarLinks('Login','login_page'))
	
	var_dict['nav_bar_list'] = links_list
	return render_to_response(template_name,var_dict,context_instance)

def view_all_articles_by_user(request,blog_name,page_number=1):
	
	#pg = (int(page_number)-1)*10          Disable partial view temporarily
	try:
		usr = User.objects.get(username=blog_name)
	except User.DoesNotExist:
		raise Http404
	
	articles = usr.article_set.all().filter(status=Article.LIVE) #[pg:pg+10]
	
	return render_with_navlist(request,'view_blog_template.html',{'articles':articles,'username':blog_name},context_instance=RequestContext(request))
	
	#~ return render_to_response('view_blog_template.html',{'articles':articles,'username':blog_name},context_instance=RequestContext(request))
	
	
def view_particular_blogpage(request,blog_name,pg_name):
	
	try:
		#~ usr = User.objects.get(username=blog_name)		
		#~ print usr.article_set.all()
		#~ art = usr.article_set.filter(slug=pg_name)
		
		art = Article.author_objects.user_articles(blog_name).filter(slug=pg_name)
		if len(art) == 0 :
			raise Http404	
		return render_with_navlist(request,'individual_article_template.html',{'p':art[0],'username':blog_name},context_instance=RequestContext(request))
				
	except User.DoesNotExist:
		raise Http404
	
def get_new_button_link(template_name,d=dict()):
	nav = NavBarLinks('',template_name,d,'')
	return nav.get_absolute_url()	

@login_required
def profile_view(request,user_name):
	
	articles_are_there = True;
	if request.user.username == user_name:
		art = Article.author_objects.user_articles(user_name).filter(status= Article.DRAFT)
		published = Article.author_objects.user_articles(user_name).filter(status= Article.LIVE)
		
		if len(art)==0 and len(published)==0:
			articles_are_there = False;
				
		l = []
		for a in art:
			u = NavBarLinks('','article_edit',{'user_name':user_name,'article_slug':a.slug})
			temp = { 'title':a.title,'edit_url':u.get_absolute_url(),'date':a.time_posted }
			l.append(temp)
			
		published_article = []
		
		for p in published:
			u = p.get_absolute_url()
			edit_link = get_new_button_link('article_edit',{'user_name':user_name,'article_slug':p.slug})
			delete_link = get_new_button_link('article_delete',{'user_name':user_name,'article_slug':p.slug})
			temp = { 'title':p.title,'url': u ,'time_posted':p.time_posted,'edit_link':edit_link,'delete_link':delete_link,}
			published_article.append(temp)
			
		link = get_new_button_link('new_article',{'user_name':user_name})
		
		
		return render_with_navlist(request,'profile_page_template.html',{'new_button_link':link,'gt_than_zero':articles_are_there,'article_drafts':l,'article_published':published_article,'username':user_name},
																									context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(get_new_button_link('profile_view',{'user_name':request.user.username}))

@login_required
def article_edit(request,user_name,article_slug):
	if request.user.username != user_name:
		raise Http404
		
	try:
		art = Article.objects.get(slug = article_slug);
	except Article.DoesNotExist:
		raise Http404

	
	if request.method == 'POST':
		f = ArticleForm(instance=art, data=request.POST)
		
		if f.is_valid():			
			new_art = f.save(commit=False)
			new_art.author = request.user;
			new_art.time_posted = datetime.now()
			new_art.save()
			return HttpResponseRedirect(new_art.get_absolute_url())			
	else:		
		f = ArticleForm(instance=art)
	
	req_context = RequestContext(request,{
											'form':f,
											})
	link = get_new_button_link('new_article',{'user_name':user_name})
	return render_with_navlist(request,'edit_page_template.html',{'username':user_name,'new_button_link':link,},req_context)
												
@login_required
def article_new(request,user_name):
	if request.user.username != user_name:
		raise Http404
		
	if request.method == 'POST':
		f = ArticleForm(data = request.POST)
		if f.is_valid():
			obj = f.save(commit=False)
			obj.author = request.user;			
			obj.time_posted = datetime.now()
			obj.save()
			return HttpResponseRedirect(obj.get_absolute_url())		
	else:
		f = ArticleForm()
		
	req_context = RequestContext(request,{
											'form':f,
											})
	link = get_new_button_link('new_article',{'user_name':user_name})
	return render_with_navlist(request,'edit_page_template.html',{'username':user_name,'new_button_link':link,},req_context)
	
@login_required
def article_delete(request,user_name,article_slug):
	if request.user.username != user_name:
		return Http404
		
	Article.author_objects.user_articles(user_name).filter(slug = article_slug).delete();
	return HttpResponseRedirect('/user/%s/'%(user_name,))
