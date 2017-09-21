from django.conf.urls import url
from .views import TokenViews, UserViews

token_create = TokenViews.as_view({
    'post': 'post'
})

token_detail = TokenViews.as_view({
    'get':  'get',
})

user_create = UserViews.as_view({
    'post': 'post'
})

user_detail = UserViews.as_view({
    'get': 'get',
    'put': 'put',
})

urlpatterns = [
    url(r'^auth/?$', token_create),
    url(r'^auth/(?P<token>.+)/$', token_detail),
    url(r'^user/?$', user_create),
    url(r'^user/(?P<username>.+)/$', user_detail)
]
