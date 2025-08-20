from django.contrib import admin

try:
    from django.conf.urls import include, url
except ImportError:
    from django.urls import re_path as url
    from django.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls'))
]
