from django.conf.urls import patterns, url
from .views import BuildingListView, BuildingDetailView, FloorListView, FloorDetailView


urlpatterns = [
    url(r'^$', BuildingListView.as_view(), name="building_rest_list"),
    url(r'^(?P<pk>\d+)/$', BuildingDetailView.as_view(), name="building_rest_detail"),
    url(r'^(?P<pk_building>\d+)/floors/$', FloorListView.as_view(), name="floor_rest_list"),
    url(r'^(?P<pk_building>\d+)/floors/(?P<pk>\d+)/$', FloorDetailView.as_view(), name="floor_rest_detail"),
]
