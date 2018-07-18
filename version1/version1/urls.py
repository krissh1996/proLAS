
from django.conf.urls import include, url
from django.contrib import admin
from GWA.forms import LoginForm
from django.contrib.auth import views
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.conf.urls.static import static

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('GWA.urls')),
    url(r'^login/$', login_forbidden(views.login), {'template_name': 'user_login.html', 'authentication_form': LoginForm}, name='login',),
    url(r'^logout/$', views.logout, {'next_page': '/login'}, name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)