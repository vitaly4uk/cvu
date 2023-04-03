"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.http import FileResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import TemplateView

def serve_favicon(request):
    return FileResponse(staticfiles_storage.open('img/favicon/favicon.ico'), content_type='image/ico')


def add_admin():
    if settings.DEBUG:
        return [
            path('admin/', admin.site.urls),
            path('ckeditor/', include('ckeditor_uploader.urls')),
        ]
    else:
        return []

urlpatterns = add_admin() + [
    path('favicon.ico', serve_favicon),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('it-rat-5d7704d9f3226c09eda298ad75522e86.txt',
         TemplateView.as_view(template_name='verification/it-rating.html', content_type='text/plain')),
    path('', TemplateView.as_view(template_name='index.html'), name='index_url'),
]
