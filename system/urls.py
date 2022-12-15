"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.urls import include
from ugo import views as views_ugo

from user import views as views_user
from user.views import ListUsers
from user.views import CreateUser
from user.views import EditUser
from user.views import EditUser

from historic_register import views as views_historic_register
from historic_register.views import ListRegistroHistorico

from report import views as views_report
from report.views import ReportRatings

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_ugo.home, name='home'),
    path('login/', views_ugo.Login.as_view(), name='login'),
    path('logout/', views_ugo.logout, name='logout'),
    path('users', ListUsers.as_view(), name='users'),
    path('users/create', CreateUser.as_view(), name='create'),
    path('delete/<int:id>', views_user.delete_user, name='delete'),
    path('users/edit/<int:pk>', EditUser.as_view(), name='edit'),
    path('users/import', views_user.upload_user, name='import'),
    path('historico', ListRegistroHistorico.as_view(), name='historico'),
    path('historico/import', views_historic_register.upload_historico, name='historicoImport'),
    path('historico/delete/<int:id>', views_historic_register.delete_historico, name='deleteHistorico'),
    path('rptHabilitaciones', ReportRatings.as_view(), name='rptHabilitaciones'),
    path('rptHabilitaciones/data', views_report.get_data_ratings, name='rptHabilitaciones-data'),
    path('rptHabilitaciones/export/<str:periodo>/<int:sede>/<int:escuela>', views_report.export_data, name='rptHabilitaciones-export'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
