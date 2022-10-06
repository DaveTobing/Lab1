from asyncore import write
import datetime
from pyexpat import model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from wishlist.models import BarangWishlist
from django.http import JsonResponse
import json


# Collaborator : Alek Yoanda Partogi Tampubolon

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


@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
    'list_barang': data_barang_wishlist,
    'nama': 'Dave Matthew Peter Lumban Tobing',
    'last_login': request.COOKIES['last_login']
    }
    return render(request, "wishlist.html", context)


def show_wishlist_ajax(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
    'list_barang': data_barang_wishlist,
    'nama': 'Dave Matthew Peter Lumban Tobing',
    'last_login': request.COOKIES['last_login']
    }
    return render(request, "wishlist_ajax.html", context)

def ajax_submit(request):
    fetch_data = json.load(request)

    data_nama = fetch_data['Barang']
    data_harga = fetch_data['Harga']
    data_deskripsi = fetch_data['Deskripsi']

    new_wishlist = BarangWishlist.objects.create(nama_barang= data_nama, harga_barang= data_harga, deskripsi= data_deskripsi)

    data = {
        "model": "wishlist.BarangWishlist",
        "pk": new_wishlist.id,
        "fields":{
            "nama_barang": data_nama,
            "harga_barang": data_harga,
            "deskripsi": data_deskripsi
        }
    }

    write_json(data)
    
    return JsonResponse(data)

# function to add to JSON
def write_json(new_data, filename='wishlist/fixtures/initial_wishlist_data.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    response.delete_cookie('last_login')
    return response

