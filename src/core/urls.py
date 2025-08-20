try:
    from django.conf.urls import include, url
except ImportError:
    from django.urls import re_path as url
    from django.urls import include

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
	# / - index page
    url(r'^$', views.recognize, name = "recognize"),
    # /about - aboutpage
    url(r'^about$', views.about, name = "about"),
    # /contribute - page with possibility to upload image to site's library
    url(r'^contribute$', views.contribute, name = "contribute"),
    # /recognize - page with actual recognition 
    url(r'^recognize$', views.recognize, name = "recognize"),
]

