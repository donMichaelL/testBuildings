from django.conf.urls import patterns, url
from .views import AccountLoginView


urlpatterns = [
    url(r'^login/$', AccountLoginView.as_view(), name="account_login"),
]
