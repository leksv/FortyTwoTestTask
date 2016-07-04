from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^', include('apps.hello.urls', namespace='hello')),

    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
