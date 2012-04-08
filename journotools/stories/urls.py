#The URL declarations for this Django project; a "table of contents" of your Django-powered site. 
#You can read more about URLs in URL dispatcher here: http://docs.djangoproject.com/en/dev/topics/http/urls/

from django.conf.urls.defaults import *
import django.contrib.auth.views

urlpatterns = patterns('stories.views',
	(r'^$','index'),
	#LOGIN PAGES
	(r'^login_page$','login_page'),
	(r'^register$','register'),
	(r'^login_submit$','login_submit'),
	(r'^logout_view$','logout_view'),
	(r'^login_error$','login_error'),
	(r'^account_disabled$','account_disabled'),
	(r'^profile','profile'),
	#STORIES
	(r'^stories/$','stories'),
	(r'^stories/add$','add'),
	(r'^stories/add_submit','add_submit'),
	(r'^stories/add_source_api$','add_source_api'),
    (r'^stories/(?P<article_id>\d+)/$', 'detail'),
	(r'^stories/(?P<article_id>\d+)/edit$', 'edit'),
	(r'^stories/(?P<article_id>\d+)/edit_submit', 'edit_submit'),
	(r'^stories/(?P<article_id>\d+)/delete$', 'delete'),
	(r'^stories/(?P<article_id>\d+)/delete_submit$', 'delete_submit'),
	(r'^stories/(?P<article_id>\d+)/status_edit$', 'status_edit'),	
	(r'^stories/(?P<article_id>\d+)/category_edit$', 'category_edit'),
	#SOURCES
    (r'^sources/$','sources_index'),
	(r'^sources/source_query$','source_query'),
	(r'^sources/add$','sources_add'),
	(r'^sources/add_submit$','sources_add_submit'),
    (r'^sources/(?P<source_id>\d+)/$', 'sources_detail'),
	(r'^sources/(?P<source_id>\d+)/edit$', 'sources_edit'),
	(r'^sources/(?P<source_id>\d+)/edit_submit$', 'sources_edit_submit'),
	(r'^sources/(?P<source_id>\d+)/delete$', 'sources_delete'),
	(r'^sources/(?P<source_id>\d+)/delete_submit$', 'sources_delete_submit'),
)