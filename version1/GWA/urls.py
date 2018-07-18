from django.conf.urls import url
from django.contrib import admin
from . import views
from GWA.forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import user_passes_test


login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')


urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^$', views.welcome, name='WelcomePage'),
    url(r'^home/', views.home, name='home'),
    url(r'^file/options/', views.plot, name='plot'),
    url(r'^submit/', views.submit, name='submit'),
    url(r'^register/$', login_forbidden(views.user_register), name='register'),
    url(r'^reset_password', views.reset_password, name='reset_password'),
    url(r'^activate', views.activate, name='activate'),
    url(r'^change_password', views.change_password, name='change_password'),
    #url(r'^crossplot/$', views.profile_update, name='profile_update'),
    url(r'^uploads/form/$', views.simple_upload, name='simple_upload'),
    url(r'^any/', views.any, name='any'),
    url(r'^crossplot/', views.crossplot, name='crossplot'),
    url(r'^doublesubmit/', views.doublesubmit, name='doublesubmit'),

]
