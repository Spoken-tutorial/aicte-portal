from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'aicte.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^portal/', include('portal.urls', namespace='portal')),

    url(r'^admin/', include(admin.site.urls)),

    # User account urls
    url(r'^accounts/login/', 'aicte.views.user_login', name='user_login'),
    url(r'^accounts/logout/', 'aicte.views.user_logout', name='user_logout'),
    url(r'^accounts/register/', 'aicte.views.user_register', name='user_register'),
)
