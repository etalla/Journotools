from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^$','stories.views.index'),
    (r'^admin/', include(admin.site.urls)),
	#(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
	#	{'document_root': 'C:\Users\eva\Dropbox\Programming\Jounotools\journotools\site_media'}),
	(r'^', include('stories.urls')),
)

urlpatterns += patterns('',
	(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)