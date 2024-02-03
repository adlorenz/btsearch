from django.urls import include, path
from django.contrib import admin
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('btsadmin/', admin.site.urls),
    path('bts/', include('btsearch.bts.urls')),
    path('map/', include('btsearch.map.urls')),
    path('panel/', include('btsearch.panel.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
