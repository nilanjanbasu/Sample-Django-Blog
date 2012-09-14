from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from markdown import markdown
# Create your models here.

class AuthorManager(models.Manager):
	def user_articles(self,username):
		return self.filter(author__username=username)#.order_by('-time_posted')

class Article(models.Model):
	
	LIVE = 1
	DRAFT = 2
	HIDDEN = 3
	
	DOC_CHOICES = (
					(LIVE,'Live'),
					(DRAFT,'Draft'),
					(HIDDEN,'Hidden'),
				)
	
	title = models.CharField(max_length=250,help_text="Maxmimum 250 characters")
	slug = 	models.SlugField(max_length = 50,help_text="Enter an unique value for using in url")
	raw_content =  models.TextField(verbose_name='Markdown Content')
	raw_snippet = models.TextField(blank=True,verbose_name='Short Description',help_text='Enter in plain text')
	time_posted = models.DateTimeField(default=datetime.now)
	status = models.IntegerField(choices=DOC_CHOICES,
								   default = LIVE,
								   help_text = 'Article will be visible only if "live" option is selected'
								   )
	author = models.ForeignKey(User)
	content_html = models.TextField(editable=False,blank=True)
	
	objects = models.Manager()
	author_objects = AuthorManager()
	
	class Meta:
		ordering = ['-time_posted']
		
	def __unicode__(self):
		return self.title
	
	def save(self,force_insert=False,force_update=False):
		self.content_html = markdown(self.raw_content)
		super(Article,self).save(force_insert,force_update)
		
	@models.permalink	
	def get_absolute_url(self):
		return ('insta_blog.views.view_particular_blogpage',(),
								{'blog_name':self.author.username,
								 'pg_name' : self.slug
								 })
	
	
