"""gtcrew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

urlpatterns = [
    path('team/', include('team.urls')),
    re_path(r'^admin/autocomplete/', include(autocomplete_admin_urls)),
    path('admin/', include('allauth.urls')),
    re_path(r'^admin/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    path('event/', include('event.urls')),
    path('story/', include('story.urls')),
    path('asset/', include('asset.urls')),
    path('feedback/', include('feedback.urls')),
    path('summernote/', include('django_summernote.urls')),
    # path('activity/', include('actstream.urls')),
    path('django_admin/', admin.site.urls),
    path('robots.txt', include('robots.urls')),
    re_path(r'', include(wagtail_urls)),
]
