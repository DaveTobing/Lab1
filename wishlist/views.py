from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from wishlist.models import BarangWishlist

# Create your views here.
def show_xml(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_xml_by_id(request):
   data = BarangWishlist.objects.filter(pk=1)
   return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")



def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
    'list_barang': data_barang_wishlist,
    'nama': 'Dave Matthew Peter Lumban Tobing'}
    return render(request, "wishlist.html", context)



