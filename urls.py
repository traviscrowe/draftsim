from django.conf.urls.defaults import *
from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns('',

    # home
    (r'^$', 'league.views.HomePage'),

    # draft picks page
    (r'draft-picks/$', 'league.views.DraftPicksPage'),

    # position page
    (r'position/(?P<position>.*)/$', 'league.views.PositionPage'),

    # admin
    (r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
  urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
