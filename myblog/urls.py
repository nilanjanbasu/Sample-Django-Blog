from django.conf.urls.defaults import patterns, include, url
from myblog import insta_blog
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myblog.views.home', name='home'),
    # url(r'^myblog/', include('myblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','insta_blog.views.login_serve'),
    url(r'^login/$','insta_blog.views.login_serve',name='login_page'),
    url(r'^logout/$','insta_blog.views.log_out_serve',name='logout_page'),
    url(r'^user/(?P<user_name>[^/]+)/$','insta_blog.views.profile_view',name='profile_view'),
    url(r'^user/(?P<user_name>[^/]+)/edit/(?P<article_slug>[^/]+)/$','insta_blog.views.article_edit',name='article_edit'), #a '/' in article will intriduce bugs (FIX)
    url(r'^user/(?P<user_name>[^/]+)/delete/(?P<article_slug>[^/]+)/$','insta_blog.views.article_delete',name='article_delete'),
    url(r'^user/(?P<user_name>[^/]+)/new/$','insta_blog.views.article_new',name='new_article'),
    url(r'^blog/(?P<blog_name>[^/]+)/(?P<page_number>\d+)/$','insta_blog.views.view_all_articles_by_user'),    
    url(r'^blog/(?P<blog_name>[^/]+)/(?P<pg_name>[^/]+)/$','insta_blog.views.view_particular_blogpage'),
)
