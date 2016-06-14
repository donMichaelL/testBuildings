from django.conf.urls import patterns, url
from .views import AccountLoginView, AccountLogoutView


urlpatterns = [
    url(r'^login/$', AccountLoginView.as_view(), name="account_login"),
    url(r'^logout/$', AccountLogoutView.as_view(), name="account_logout"),
]
