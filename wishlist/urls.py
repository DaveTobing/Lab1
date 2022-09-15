from django.urls import path
from wishlist.views import show_wishlist, show_xml, show_json,show_xml_by_id

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('xml/', show_xml, name='show_xml'), #sesuaikan dengan nama fungsi yang dibuat
    path('json/', show_json, name='show_json'), #sesuaikan dengan nama fungsi yang dibuat
    path('xml/1', show_xml_by_id, name='show_xml_by_id'), #sesuaikan dengan nama fungsi yang dibuat
]