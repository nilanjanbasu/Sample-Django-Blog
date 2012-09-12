from django.conf.urls.defaults import *

urlpatterns = patterns('',
						(r'^$','myblog.insta_blog.views.login_serve'),
)
						
