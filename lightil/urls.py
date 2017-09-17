from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from jwt_auth.views import TokenCreateViews, TokenVerifyDeleteViews

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/$', TokenCreateViews.as_view()),
    url(r'^api/auth/(?P<token>.+)/$', TokenVerifyDeleteViews.as_view()),
    url(r'^api/', include(router.urls, namespace='api'))
]
