"""gtcrew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""
from allauth.account.views import LoginView, LogoutView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

urlpatterns = [
    path('team/', include('team.urls')),
    path('account/', include('allauth.urls')),
    re_path(r'^admin/autocomplete/', include(autocomplete_admin_urls)),
    re_path(r'^admin/login/$', LoginView.as_view(), name='wagtailadmin_login'),
    re_path(r'^admin/logout/$', LogoutView.as_view(), name='wagtailadmin_logout'),
    re_path(r'^admin/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    path('story/', include('story.urls')),
    path('asset/', include('asset.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('django_admin/', admin.site.urls),
    re_path(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path('', include(wagtail_urls)),
]
