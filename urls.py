from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('PloneBackupRecoverManagement.auth.views',
    #(r'^$', 'login'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
)

urlpatterns += patterns('PloneBackupRecoverManagement.recover.views',
    # Examples:
    # url(r'^$', 'PloneBackupRecoverManagement.views.home', name='home'),
    # url(r'^PloneBackupRecoverManagement/', include('PloneBackupRecoverManagement.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^recover/$', 'index'),
    (r'^recover/do/$', 'do_command'),
    (r'^recover/can_delete/(?P<filename>[\d\-]+\.(fsz|deltafsz))/$', 'can_delete'),
)

urlpatterns += patterns('PloneBackupRecoverManagement.backup.views',
    (r'^backup/$', 'index'),
)

urlpatterns += patterns('PloneBackupRecoverManagement.configuration.views',
    (r'^configure/$', 'index'),
)

urlpatterns += patterns('PloneBackupRecoverManagement.logger.views',
    (r'^log/$', 'index'),
)
