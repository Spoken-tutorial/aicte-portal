from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aicte.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'portal.views.home', name='home'),
    url(r'^extension/$', 'portal.views.extension', name='extension'),
    
    #Ajax
    url(r'^ajax-state/$', 'portal.views.ajax_state', name='ajax_state'),
    url(r'^ajax-location/$', 'portal.views.ajax_location', name='ajax_location'),
    url(r'^ajax-pincode/$', 'portal.views.ajax_pincode', name='ajax_pincode'),
)
