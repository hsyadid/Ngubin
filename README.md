# toko_ngubin

## Link PWS

Web dapat diakses melalui <http://hubban-syadid-ngubin.pbp.cs.ui.ac.id/>

# SOAL TUGAS 3

## Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?

> Proses data delivery menjadi aspek penting dalam pengembangan sebuah platform dikarenakan, seringkali platform yang kita buat ingin berkomunikasi dengan sebuah sistem lain melalui sebuah API dan semacamnya, data delivery memastikan data dikirim dan juga diterima dalam bentuk yang dapat di akses dan diproses oleh berbagai sistem, contoh nya adalah menggunakan XML dan juga JSON.

## Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?

> Dikarenakan format JSOn lebih flexibel dan juga mudah diolah dibandingkan bentuk XML. JSON memiliki struktur yang sederhana dan mudah untuk dibaca oleh manusia.Struktur yang diimplementasikan oleh JSON adalah key-value pair yang mana ini berbeda dengan XML yang memiliki tag penutup dan pembuka. Dari segi parsing pun JSON lebih cepat untuk di parse daripada XML ini berakibat dari strukturnya yang sederhana. Ukuran file json pun biasanya juga lebih kecil jika dibandingkan dengan XML

## Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?

> Dikarenakan method ini berfungsi untuk mengecek apakah input yang telah dimasukkan oleh user telah sesuai atau belum dengan kriteria yang telah di kita definisikan dalam form sebelumnya, seperti panjang string maupun angka dalam rentang tertentu.dan jika kiat tidak mengimplementasikan method ini kita tidak bisa memberikan umpan balik kesalahan yang jelas kepada pengguna.

## Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?

> Pada saat data delivery `csrf_token` di peruntukan untuk aspek keamanan contoh yang dapat membahayakan aplikasi contoh nya adalah serangan CSRF (Cross-Site Request Forgery). Pada serangan ini penyerang bisa saja membuat request yang tampak nya valid dari sumber yang sebenarnya tidak sah. Dan cara kerja dari pun cukup mudah dimengerti dengan menambahkan token CSRF ke dalam formulir, nantinya django bisa memverifikasi apakah kode ini berasal dari sesi pengguna yang sama atau tidak.

> Jika kita tidak menambahkan csrf_token pada form yang kita buat, tentu aplikasi kita akan rentan terhadap serangan CSRF, yang mana ini berbahaya dikarenakan penyerang dapat mengubah pengaturan akun pengguna atau pun melakukan transaksi finansial atau mengirimkan data yang tidak diinginkan tanpa sepengetahuan dari pengguna. Kesimpulan penggunaan `csrf_token` itu penting untuk menghindari eksploitasi data pribadi.

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial) ?

1. Saya mengimplementasikan perubahan dengan menambahkan atribut `ID` kedalam model saya, lalu menjalankan `python manage.py makemigrations` dan python `manage.py migrate.`<br>

```from django.db import models
import uuid

# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

2. Membuat `forms.py` pada direktori main django dan menambahkan model yang telah kita miliki<br>

```
from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description']
```

3.Mengupdate kode untuk function `home` yang terdapat di `view.py` dan menambhakan function baru seperti `create_product` `show_xml_data` `show_json_data` `show_xml_by_id` `show_json_bt_id`

```
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from main.models import Product
from main.forms import ProductForm

# Create your views here.
def home(request):
    Products = Product.objects.all()
    detail = {
        'nama_apps': 'Ngubin E-commerce',
        'nama_mahasiswa': 'Hubban Syadid',
        'kelas' : 'PBP-A',
        'Products': Products
    }

    return render(request, 'main.html', detail)

def create_product(request):
    form = ProductForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        print("form is valid")
        form.save()
        return redirect('/')
    else:
        print("form is not valid")
        print(form.errors)

    detail = {
        'form': form
    }

    return render(request, 'create_product.html', detail)


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
```

4. Menkonfigurasikan function yang telah kita buat tersebut dengan endpoint yang beda pada `urls.py` di dalam `main`

```
....
from  main.views import home, create_product, show_xml_data, show_json_data, show_xml_by_id, show_json_by_id

urlpatterns = [
....
    path('create_product/', create_product, name='create_product'),
    path('xml_data/', show_xml_data, name='show_xml_data'),
    path('json_data/', show_json_data, name='show_json_data'),
    path('xml_data/<id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json_data/<id>/', show_json_by_id, name='show_json_by_id'),
]
```

5. Membuat template HTML yang nantinya akan di gunakan pada semua html proyek dengan nama `base.html` yang terdapat di `ROOT FILE` dan langsung mengunakanya pada `main.html` yang terdapat di `main`

`base.html`

```
{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    {% block meta %} {% endblock meta %}
  </head>

  <body>
    {% block content %} {% endblock content %}
  </body>
</html>
```

`main.html`

```
{% extends 'base.html' %}
{% block content %}
<h1>{{nama_apps}}</h1>
<div class="detail_info">
    <p>{{nama_mahasiswa}}</p>
    <p>{{kelas}}</p>
</div>

{% if not Products %}
<p>There is no product</p>
{% else %}
<table>
    <tr>
        <th>name</th>
        <th>price</th>
        <th>category</th>
        <th>description</th>
    </tr>
    {% for product in Products %}
<tr>
    <td>{{product.name}}</td>
    <td>{{product.price}}</td>
    <td>{{product.category}}</td>
    <td>{{product.description}}</td>
</tr>
{% endfor %}
</table>
{% endif %}

<a href="{% url 'main:create_product' %}">
    <button>Add Product</button>
  </a>

{% endblock content %}
```

6. Menambahkan lokasi direktori tersebut ke dalam settings.py di direktori `toko_ngubin`.

```
   ...
   'DIRS': [BASE_DIR / 'templates'],
   ...
```

7. Menguji aplikasi Django secara langsung di browser dengan alamat default http://127.0.0.1:8000/dengan run `python manage.py runserver`.

## Contoh http response mengunakan metode get

1. XML <br>
   ![xml](media/xml_data.jpg)

2. JSON <br>
   ![json](media/json_data.jpg)

3. XMl Filter id<br>
   ![xml_id](media/xml_id.jpg)

4. JSON Filter id<br>
   ![json_id](media/json_id.jpg)

# SOAL TUGAS 4

## Apa perbedaan antara HttpResponseRedirect() dan redirect()?

> Secara fungsi, kedua fungsi tersebut memiliki tujuan yang sama yaitu untuk mengarahkan pengguna ke halaman tertentu. Namun, kelemahan dari HttpResponseRedirect() adalah bahwa developer harus menyertakan path absolut jika ingin mengarahkan pengguna ke halaman tersebut. Apabila developer ingin memanggil metode atau model yang ada di urls.py hanya dengan menyertakan namanya saja, mereka perlu menggunakan metode reverse(). Sebaliknya, dengan redirect(), developer bisa langsung memberikan nama metode sesuai di urls.py tanpa harus menyertakan path absolutnya.

## Jelaskan cara kerja penghubungan model Product dengan User!

> Cara menghubungkanya dengan mengunakan relational database, karena disini konteks dari usernya adalah mengunakan model `user` yang disediakan oleh django. kita dapat mengubungkan `user` di dalam model yang telah kita buat dengan memasukanya sebagai foreign key pada model product yang nantinya foreign key ini mengacu pada model user

## Apa perbedaan antara authentication dan authorization, apakah yang dilakukan saat pengguna login?

> perbedaanya adalah authentication adalah proses memverifikasi identitas pengguna. Ini memastikan bahwa pengguna yang berusaha masuk benar-benar sesuai dengan data yang mereka klaim. Proses ini biasanya melibatkan validasi kredensial seperti username dan password.

> authorization adalah proses yang terjadi setelah authentication berhasil. Authorization menentukan apa yang boleh atau tidak boleh diakses oleh pengguna tersebut di dalam sistem. Proses ini mengatur hak akses dan otoritas pengguna terhadap sumber daya tertentu.

## Jelaskan bagaimana Django mengimplementasikan kedua konsep tersebut ?

> secara default django telah menyediakan sistem aunthetication bawaan yang memudahkan developer untuk memverifikasi penguna tanpa harus membuat nya dari awal lagi, sistem seperti model user yang berisi akan informasi seperti username, password yang telah dienkripsi, dan sebagainya bisa langsung kalian gunakan dan hubungkan kedalam model anda.

> bukan hanya itu saya django juga telah menyediakan login function yang akan mencatat sesi pengguna jika sudah ter aunthentikasi, kalian juga bisa mengatur bagaimana verifikasi pengguna melalui function authenticate()

> untuk konsep authorization pada django juga sudah ada secara default contohnya adalah yang digunakan pada tugas kali ini yaitu @login_required yang akan memastikan hanya pengguna yang telah login saja yang boleh mengakses halam tertentu

## Bagaimana Django mengingat pengguna yang telah login? Jelaskan kegunaan lain dari cookies dan apakah semua cookies aman digunakan?

> setelah user telah berhasil login, django dapat membuat session id untuk setiap pengguna yang mana berisi informasi terkait user yang login, nanti nya session ID ini di simpan dalam cookie ke browser, jika user melakukan pengguna request baru, secara otomatis browser akan mengirimi session ID ini dan akan mencocokanya dengan data session di server. cara ini dilakukan agar pengguna tidak perlu login atau memasukan kredensial lagi

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

1. Saya membuat method yang menghandle untuk registrasi yang mengunakan fungsi bawaan pada modul django yaitu `UserCreationForm` pada `view`, dan bukan hanya itu saya juga membuat html yang mana jika user ingin melakukan registrasi akan di arahkan ke halaman tersebut

`view`

```
from django.contrib.auth.forms import UserCreationForm

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

```

`register.html`

```
{% extends 'base.html' %}

{% block meta %}
<title>Register Penjual</title>
{% endblock meta %}

{% block content %}

<div class="login">
  <h1>Register</h1>

  <form method="POST">
    {% csrf_token %}
    <table>
      {{ form.as_table }}
      <tr>
        <td></td>
        <td><input type="submit" name="submit" value="Daftar" /></td>
      </tr>
    </table>
  </form>

  {% if messages %}
  <ul>
    {% for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
  </ul>
  {% endif %}
</div>

{% endblock content %}
```

2.Fitur selanjutnya yang saya buat adalah fitur login, saya juga mengimplementasikan penyimpanan cookies untuk mengelola sesi pengguna. Fitur ini akan saya terapkan di dalam fungsi `view`. Selain itu, saya juga membuat halaman HTML khusus untuk formulir login, untuk pengguna memasukkan kredensial mereka.

`view`

```
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
import datetime

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
```

`login.html`

```
{% extends 'base.html' %}

{% block meta %}
<title>Login</title>
{% endblock meta %}

{% block content %}
<div class="login">
  <h1>Login</h1>

  <form method="POST" action="">
    {% csrf_token %}
    <table>
      {{ form.as_table }}
      <tr>
        <td></td>
        <td><input class="btn login_btn" type="submit" value="Login" /></td>
      </tr>
    </table>
  </form>

  {% if messages %}
  <ul>
    {% for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
  </ul>
  {% endif %} Don't have an account yet?
  <a href="{% url 'main:register' %}">Register Now</a>
</div>

{% endblock content %}
```

3.Setelah membuat fitur login dan register selanjutnya, saya akan membuat fitur logout pada `view` yang mana fitur ini secara otomatis akan menghapus cookies pada web anda juga. saya menambahkan beberapa tambahan pada `main.html` untuk menampilkan button logout.

`view`

```
from django.contrib.auth import authenticate, login, logout

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
```

`main.html`

```
...
<a href="{% url 'main:logout' %}">
  <button>Logout</button>
</a>
...

```

4. Setelah mengimplementasikan cookies pada login dan juga logout, saya ingin menampilkan datetime kapan saya login pada `main.html`, oleh karena itu saya menambahkan beberapa tambahan

`main.html`

```
...
<h5>Sesi terakhir login: {{ last_login }}</h5>
...

```

5. Langkah terakhir adalah menambahkan fungsi yang sudah saya buat di dalam `view` ke dalam `urls.py` yang terdapat pada `main`, agar nantinya fungsi tersebut bisa dipanggil ketika diakses melalui URL yang sesuai.

`urls.py`

```
from main.views import register, login_user, logout_user

    ...
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    ...

```

6. Ada tambahan untuk proyek ini terkait pada PWS nantinya, pada bagian `settings.py`

```
import os

PRODUCTION = os.getenv("PRODUCTION", False)
DEBUG = not PRODUCTION
```
