from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'urlshot.views.home', name='home'),
    # url(r'^urlshot/', include('urlshot.foo.urls')),
    url(r'^$', 'urlshot.urlshot_app.views.get', name='home'),
    url(r'^api/([a-zA-Z0-9#@=/_$.:-]+)$', 'urlshot.urlshot_app.views.getJSON'),
    url(r'^[a-zA-Z0-9]+/?$', 'urlshot.urlshot_app.views.redirect_url'),
    #url(r'^.+$', 'urlshot.urlshot_app.views.get', name='home'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
