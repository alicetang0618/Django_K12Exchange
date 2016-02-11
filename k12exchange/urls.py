from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
import settings

urlpatterns = patterns('',
    url(r'^$', 'application.views.home', name = 'home'),
    url(r'^join/$', 'application.views.join', name = 'join'),
    url(r'^login/$', 'application.views.login', name = 'login'),
    url(r'^logout/$', 'application.views.logout', name = 'logout'),
    url(r'^my_profile/$', 'application.views.my_profile', name = 'my_profile'),
    url(r'^modify_profile/$', 'application.views.modify_profile', name = 'modify_profile'),
    url(r'^profile/(?P<user_id>\d+)/$','application.views.profile',name='profile'),
    url(r'^my_materials/$', 'application.views.my_materials', name = 'my_materials'),
    url(r'^material/(?P<material_id>\d+)/$', 'application.views.material', name = 'material'), 
	url(r'^my_downloads/$', 'application.views.my_downloads', name = 'my_downloads'),
	url(r'^like/$', 'application.views.like', name = 'like'),
	url(r'^my_messages/$','application.views.my_messages',name='my_messages'),
    url(r'^message/(?P<message_id>\d+)/$','application.views.message',name='message'),
    url(r'^search/(?P<search_id>\d+)/$', 'application.views.search', name ='search'),
    url(r'^upload/$', 'application.views.upload', name='upload'),
    url(r'session_security/', include('session_security.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact/$', 'application.views.contact', name = 'contact'), 
    url(r'^privacy/$', 'application.views.privacy', name = 'privacy'), 
    url(r'^terms/$', 'application.views.terms', name = 'terms'), 
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
