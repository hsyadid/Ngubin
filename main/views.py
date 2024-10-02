from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from main.models import Product
from main.forms import ProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
import datetime



#SHOW MAIN PAGE
@login_required(login_url='/login/')
def home(request):
    Products = Product.objects.filter(user=request.user)
    detail = {
        'nama_apps': 'Ngubin E-commerce',
        'nama_mahasiswa': request.user.username,
        'kelas' : 'PBP-A',
        'NPM' : '1808561061',
        'Products': Products, 
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, 'main.html', detail)

#AUNTHENTICATION AND AUTHORIZATION FUNCTION
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun berhasil dibuat')
            return redirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:home"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


# CRUD FUNCTION
def create_product(request):
    form = ProductForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        new_product = form.save(commit=False)
        new_product.user = request.user
        new_product.save()
        return redirect('main:home')
    else:
        print("form is not valid")
        print(form.errors)

    detail = {
        'form': form
    }

    return render(request, 'create_product.html', detail)

def edit_product(request, id):
    # Get mood entry berdasarkan id
    getProduct = Product.objects.get(pk = id)

    # Set mood entry sebagai instance dari form
    form = ProductForm(request.POST or None, instance=getProduct)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:home'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    getProduct = Product.objects.get(pk = id)
    # Hapus getProduct
    getProduct.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:home'))

# TO INTERACT WITH DATABASE
def show_xml_data(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_data(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
