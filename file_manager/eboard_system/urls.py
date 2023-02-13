"""eboard_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="E-Board API's")

urlpatterns = [
    path('', include('demo.urls')),
    path('admin/', admin.site.urls),
    path('api/user/',include('accounts.urls')),
    path('api/contract/',include('contract_manager.urls')),
    path('api/voting/', include('voting.urls')),
    path('api/file-manager/', include('file_manager.urls')),
    path('api/licenses/', include('licenses.urls')),
    path('api/zoom/', include('zoom_integration.urls')),
    path('api/docs/', schema_view),
    path('api/tasks/', include('tasks.urls')),
    path('api/signature/', include('signatures.urls')),
    path('api/surveys/', include('surveys.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/compliance/', include('compliance_management.urls')),
    path('api/meeting/', include('meeting_management.urls')),

]
