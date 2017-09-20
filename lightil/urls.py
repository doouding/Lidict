from django.contrib import admin
from django.conf.urls import url, include
from jwt_auth.urls import urlpatterns as jwt_auth_patterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(jwt_auth_patterns, namespace='api')),
]
