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

# SOAL TUGAS 5

## Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!

> Pada CSS ada beberapa selector yang lebih yang diprioritaskan saat anda memilih elemen untuk diberikan style, diantara selector nya dari yang lebih didahulukan dan yang paling tidak didahulukan :

1. Inline styles
2. ID selector (Mengunakan : #)
3. Class Selector (Mengunakan : .)
4. Element selector
5. Universal selectors

> Jika dua selector dengan specificity yang sama akan di apply yang terlebih dahulu di deklarasikan

## Mengapa responsive design menjadi konsep yang penting dalam pengembangan aplikasi web? Berikan contoh aplikasi yang sudah dan belum menerapkan responsive design!

> Responsive menjadi konsep yang penting dalam pengembangan aplikasi web karena semakin banyak pengguna mengakses internet melalui berbagai perangkat dengan ukuran layar yang berbeda. Dengan menerapkan responsive design, aplikasi web dapat menyesuaikan tampilan dan tata letaknya secara otomatis sesuai dengan ukuran layar, sehingga pengalaman pengguna menjadi lebih optimal. Contoh aplikasi yang sudah menerapkan responsive design adalah Twitter, di mana tampilan antarmuka berubah sesuai dengan perangkat yang digunakan, memudahkan pengguna dalam menjelajahi konten. Di sisi lain, aplikasi seperti siak yang belum sepenuhnya menerapkan responsive design dapat membuat pengalaman pengguna menjadi kurang nyaman.

## Jelaskan perbedaan antara margin, border, dan padding, serta cara untuk mengimplementasikan ketiga hal tersebut!

> Margin, border, dan padding adalah elemen css ygy mengatur tata letak dan tampilan elemen pada halaman web. Margin merujuk pada ruang di luar batas elemen, berfungsi untuk menciptakan jarak antara elemen satu dengan yang lainnya. Sebagai contoh,

```
.element {
    margin: 20px; /* Jarak 20px di semua sisi */
}
```

> Border adalah garis yang mengelilingi elemen, yang dapat diatur ketebalan, jenis, dan warnanya, memberikan definisi visual pada elemen.

```
.element {
    border: 2px solid black; /* Border dengan ketebalan 2px, jenis solid, dan warna hitam */
}
```

> padding adalah ruang di dalam batas elemen, antara konten seperti teks atau gambar dan border, sehingga konten tidak terjepit di tepi elemen. Dengan mengatur padding, kita dapat memastikan bahwa konten memiliki ruang yang cukup di sekitarnya.

```
.element {
    padding: 15px; /* Ruang 15px di semua sisi antara konten dan border */
}

```

## Jelaskan konsep flex box dan grid layout beserta kegunaannya!

> Flexbox dan Grid Layout adalah dua model tata letak CSS yang dirancang untuk memudahkan pengaturan elemen di dalam halaman web.

> Flexbox (Flexible Box Layout) adalah metode tata letak satu dimensi yang memungkinkan elemen untuk disusun secara horizontal atau vertikal dalam sebuah wadah. Dengan menggunakan flexbox, kita dapat dengan mudah mengatur ruang, perataan, dan urutan elemen, serta menciptakan desain responsif tanpa memerlukan banyak kode.

> Sementara itu, Grid Layout adalah metode tata letak dua dimensi yang memungkinkan kita untuk membuat struktur grid dengan baris dan kolom. Grid sangat ideal untuk desain yang lebih kompleks di mana kita ingin mengatur elemen dalam bentuk tabel, seperti layout halaman yang memiliki header, konten utama, dan sidebar.

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)!

1.Berikut adalah penjelasan secara singkat tentang langkah-langkah yang telah kamu sebutkan:

1. **Menginisialisasi Tailwind di Header `base.html`:**
   Tailwind CSS adalah framework yang mempermudah styling halaman web dengan menggunakan utility classes. Menginisialisasi Tailwind di `base.html` dengan cara menambahkan referensi ke file CSS Tailwind di bagian header. Hal ini memastikan bahwa semua halaman yang mewarisi template `base.html` bisa menggunakan Tailwind untuk styling secara global.

2. **Membuat Function `edit_product` dan `delete_product` di `views.py`:**
   Function ini dibuat untuk menangani aksi edit dan hapus produk. Function `edit_product` memungkinkan pengguna mengubah detail produk melalui form yang sudah terisi sebelumnya, sementara `delete_product` bertugas untuk menghapus produk yang dipilih dari database setelah pengguna mengonfirmasi.

3. **Menyambungkan Function ke `urls.py`:**
   Setelah function untuk mengedit dan menghapus produk dibuat, kita harus menyambungkannya dengan URL yang spesifik. Dengan menambahkan jalur URL ini, kita memastikan bahwa pengguna bisa mengakses halaman edit atau hapus produk dengan cara mengunjungi URL yang sesuai di aplikasi web.

4. **Membuat dan Memberikan Style pada `Navbar`:**
   Navbar adalah elemen navigasi yang muncul di setiap halaman. Dengan merancang navbar di `main.html`, kita memastikan bahwa struktur dan gaya navigasi konsisten di seluruh halaman situs. Navbar ini kemudian di-styling menggunakan utility classes dari Tailwind agar tampak menarik dan responsif.

5. **Memberikan Style CSS Global:**
   Selain menggunakan Tailwind, saya menambahkan gaya kustom global untuk aplikasi. CSS global ini diterapkan di seluruh halaman untuk memastikan konsistensi dalam tampilan, seperti pengaturan font, warna latar, dan gaya link. Gaya ini membantu memberikan pengalaman pengguna yang seragam di seluruh aplikasi web.

# SOAL TUGAS 6

## 1. Jelaskan manfaat dari penggunaan JavaScript dalam pengembangan aplikasi web!

> Penggunaan JavaScript dalam pengembangan aplikasi web memiliki banyak manfaat yang pertama, JavaScript memungkinkan pengembang untuk menciptakan pengalaman pengguna yang interaktif dan responsif. Dengan kemampuan untuk memanipulasi elemen DOM (Document Object Model) secara real-time, JavaScript memungkinkan pembuatan elemen interaktif seperti tombol, formulir, dan efek animasi yang meningkatkan keterlibatan pengguna. Selain itu, JavaScript bekerja di sisi klien, artinya sebagian besar proses dilakukan di dalam browser tanpa perlu berulang kali berkomunikasi dengan server. Ini tidak hanya mempercepat waktu respon aplikasi, tetapi juga mengurangi beban server dan bandwidth yang diperlukan untuk mentransfer data.

> JavaScript juga memiliki ekosistem yang kaya dengan berbagai pustaka dan framework, yang mempercepat pengembangan aplikasi web modern dengan menyediakan komponen siap pakai dan alat bantu yang memudahkan pengelolaan status dan interaksi.Keunggulan lainnya adalah kemudahan integrasi dengan teknologi lain, seperti API.

## 2. Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await?

> Penggunaan await dalam konteks pemanggilan `fetch()` di JavaScript adalah untuk menangani operasi asinkron secara lebih efisien dan intuitif. Fungsi `fetch()` mengembalikan sebuah Promise, yang berarti bahwa hasil dari pemanggilan ini tidak langsung tersedia, melainkan akan tersedia di masa depan setelah proses pengambilan data selesai. Dengan menggunakan await, kita memberi tahu JavaScript untuk menunggu sampai Promise tersebut diselesaikan sebelum melanjutkan eksekusi kode di bawahnya. Dan kita dapat langsung menggunakan hasil dari `fetch()` tanpa harus menggunakan metode `.then()`.

> Jika kita tidak menggunakan await, eksekusi kode akan berjalan tanpa menunggu hasil dari `fetch()`, yang dapat mengakibatkan berbagai masalah. Salah satunya, jika kita mencoba untuk mengakses data yang diambil sebelum Promise diselesaikan, yang kita dapatkan adalah nilai undefined atau kesalahan yang menunjukkan bahwa data belum tersedia.

## 3.Mengapa kita perlu menggunakan decorator csrf_exempt pada view yang akan digunakan untuk AJAX POST?

> Penggunaan decorator csrf_exempt digunakan untuk keamanan aplikasi. Secara default, Django melindungi aplikasi dari serangan Cross-Site Request Forgery (CSRF) dengan mengharuskan setiap permintaan POST untuk menyertakan token CSRF yang valid. Dalam konteks AJAX kita membuat permintaan POST dari klien kita sering kali tidak secara otomatis menyertakan token CSRF. Jika permintaan POST dikirim tanpa token yang valid, Django akan menolak permintaan tersebut dan mengembalikan kesalahan 403 Forbidden. Hal ini dapat menyebabkan aplikasi tidak berfungsi dengan baik karena tidak dapat memproses data yang dikirim dari klien.

> Dengan menggunakan decorator csrf_exempt, kita memberi tahu Django untuk mengabaikan validasi CSRF pada view tertentu. Ini sangat berguna untuk endpoint API atau view yang secara eksklusif dirancang untuk menangani permintaan AJAX dari klien yang terpercaya.

## 4.Pada tutorial PBP minggu ini, pembersihan data input pengguna dilakukan di belakang (backend) juga. Mengapa hal tersebut tidak dilakukan di frontend saja?

> data input pengguna yang dilakukan di backend adalah langkah penting untuk menjaga keamanan dan integritas aplikasi. karena frontend dapat dengan mudah dimanipulasi oleh orang yang tidak bertanggung jawab. aplikasi menjadi rentan terhadap serangan seperti injeksi SQL atau Cross-Site Scripting (XSS).

## 5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)!

**1.Menambahkan fungsi baru kedalam `view.py` yang mana fungsi tersebut berguna untuk menambhkan product mengunakan AJAX, serta memodifikasi passing argumen untuk fungsi `home`**

```
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

...
@csrf_exempt
@require_POST
def create_product_ajax(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    category = request.POST.get("category")
    description = request.POST.get("description")
    user = request.user

    newProduct = Product(
        name=name, price=price,
        category=category,description=description,
        user=user
    )
    newProduct.save()

    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='/login/')
def home(request):
    detail = {
        'nama_apps': 'Ngubin E-commerce',
        'nama_mahasiswa': request.user.username,
        'kelas' : 'PBP-A',
        'NPM' : '1808561061',
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, 'main.html', detail)
...
```

**2.Setelah menambahkanfungsi baru lalu hubungkan lah kedalam suatu url untuk digunakan**

```
from main.views import create_product_ajax

...
    path('create_product_ajax/', create_product_ajax, name='create_product_ajax'),
....
```

**3.Menambhakan fungsi kedalam productForm kita yang berada pada `form.py` untuk nantinya bisa digunakan untuk validasi input user**

```
from django.utils.html import strip_tags

...
 def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
...
```

**4.Menambahkan button baru untuk menginput product dengan AJAX dan juga modal untuk menaruh formnya di html `main`**

```
...
    <a href="{% url 'main:create_product' %}" class="animate-pulse bg-[#2ebdaa] hover:bg-[#008776] text-white font-bold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105">
        + Product
    </a>
    <button data-modal-target="crudModal" data-modal-toggle="crudModal" class="bg-[#2ebdaa] hover:bg-[#008776] text-white font-bold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105" onclick="showModal();">
        + Product by AJAX
    </button>
...
...
<div class="relative z-5 -mt-[220px] gap-6 mb-6 ">
      <div id="product_container"></div>
    </div>

    <div id="crudModal" tabindex="-1" aria-hidden="true" class="hidden fixed inset-0 z-50 w-full flex items-center justify-center bg-gray-800 bg-opacity-50 overflow-x-hidden overflow-y-auto transition-opacity duration-300 ease-out">
        <div id="crudModalContent" class="relative bg-white rounded-lg shadow-lg w-5/6 sm:w-3/4 md:w-1/2 lg:w-1/3 mx-4 sm:mx-0 transform scale-95 opacity-0 transition-transform transition-opacity duration-300 ease-out">
          <!-- Modal header -->
          <div class="flex items-center justify-between p-4 border-b rounded-t">
            <h3 class="text-xl font-semibold text-gray-900">
              Add New Product Entry
            </h3>
            <button type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center" id="closeModalBtn">
              <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
              </svg>
              <span class="sr-only">Close modal</span>
            </button>
          </div>
          <!-- Modal body -->
          <div class="px-6 py-4 space-y-6 form-style">
            <form id="productEntryForm">
              <div class="mb-4">
                <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
                <input type="text" id="name" name="name" class="mt-1 block w-full border border-gray-300 rounded-md p-2 hover:border-indigo-700" placeholder="Enter your name" required>
              </div>
              <div class="mb-4">
                <label for="price" class="block text-sm font-medium text-gray-700">Price</label>
                <input type="number" id="price" name="price" rows="3" min="0" class="mt-1 block w-full h-10 resize-none border border-gray-300 rounded-md p-2 hover:border-indigo-700" placeholder="Enter the price" required>
              </div>
              <div class="mb-4">
                <label for="category" class="block text-sm font-medium text-gray-700">Category</label>
                <input type="text" id="category" name="category"  class="mt-1 block w-full border border-gray-300 rounded-md p-2 hover:border-indigo-700" required>
              </div>
              <div class="mb-4">
                <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
                <textarea  id="description" name="description"  class="mt-1 block w-full border border-gray-300 rounded-md p-2 hover:border-indigo-700 h-32" required></textarea>
              </div>
            </form>
          </div>
          <!-- Modal footer -->
          <div class="flex flex-col space-y-2 md:flex-row md:space-y-0 md:space-x-2 p-6 border-t border-gray-200 rounded-b justify-center md:justify-end">
            <button type="button" class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg" id="cancelButton">Cancel</button>
            <button type="submit" id="submitProduct" form="productEntryForm" class="bg-indigo-700 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg">Save</button>
          </div>
        </div>
      </div>

...
```

**5.Menambahkan fungsi javascript yang akan di gunakan untuk membuat web kita lebih dinamis**

```
...
<script>
  async function getProductEntries(){
      return fetch("{% url 'main:show_json_data' %}").then((res) => res.json())
  }

  async function refreshProduct() {
    const productCard = document.getElementById("product_container");
    productCard.innerHTML = "";
    productCard.className = "";
    const productEntries = await getProductEntries();
    console.log(productEntries); // Debugging: lihat isi productEntries
    let htmlString = "";
    let classNameString = "";

    if (productEntries.length === 0) {
        console.log("Tidak ada produk, menampilkan pesan...");

        classNameString = "flex flex-col items-center justify-center min-h-[24rem] p-6";
        htmlString = `
        <div class="flex flex-col items-center justify-center min-h-[24rem] p-6 -mt-[90px]">
            <img src="{% static 'images/sad_face.png' %}" alt="Sad face" class="w-32 h-32 w-fit "/>
            <p class="text-center text-white mt-4">Belum ada data product.</p>
        </div>
        `;
    } else {
        console.log("Ada produk, memproses data...");

        classNameString = "columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6 w-full";
        productEntries.forEach((item) => {
            const name = DOMPurify.sanitize(item.fields.name);
            const description = DOMPurify.sanitize(item.fields.description);
            htmlString += `
            <div class="relative break-inside-avoid h-[370px] w-[325px] rounded-3xl perspective" data-pk="{{ item.pk }}">
                <div class="container" onclick="this.classList.toggle('flipped')">
                    <!-- Card Front -->
                    <div class="card front">
                        <div class="p-6 flex flex-col justify-between items-center">
                            <div class="flex justify-between w-[270px]">
                                <a href="/edit-product/${item.pk}" class="bg-yellow-500 hover:bg-yellow-600 text-white rounded-full p-2 transition duration-300 shadow-md"  onclick="event.stopPropagation();">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                    </svg>
                                </a>

                                <p class="font-medium text-md">${item.fields.category}</p>

                                <a href="/delete/${item.pk}" class="bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition duration-300 shadow-md"  onclick="event.stopPropagation();">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                                    </svg>
                                </a>
                            </div>

                            <div class="p-3 flex justify-center items-center flex-col relative">
                                <img src="{% static 'images/ubin.png' %}" alt="foto ubin" class="h-48 w-48 relative z-10">
                                <div class="w-[270px] h-32 bg-product-radial rounded-full absolute top-[95px] z-0"></div>
                            </div>

                            <div class="mt-4 flex flex-col items-center text-center overflow-hidden h-24">
                                <p class="text-black font-bold text-md truncate">${name}</p> <!-- Gunakan line-clamp -->
                                <p class="text-gray-700 font-semibold mb-2 truncate">${item.fields.price}</p>
                            </div>

                        </div>
                    </div>

                    <!-- Card Back -->
                    <div class="card back">
                        <div class="p-6 flex flex-col justify-center items-center">
                            <h3 class="text-white text-xl font-semibold">Detail Item</h3>
                            <p class="text-gray-300 text-md mt-2 text-center">${description}</p>
                            <div class="mt-4"></div>
                        </div>
                    </div>
                </div>
            </div>`;
        });
    }

    // Set className dan innerHTML sekali di sini setelah semua proses
    productCard.className = classNameString;
    productCard.innerHTML = htmlString;
    console.log("HTML string setelah proses:", htmlString);
    console.log("Elemen product_card:", productCard);
}


  refreshProduct();

  const modal = document.getElementById('crudModal');
  const modalContent = document.getElementById('crudModalContent');

  function showModal() {
      const modal = document.getElementById('crudModal');
      const modalContent = document.getElementById('crudModalContent');

      modal.classList.remove('hidden');
      setTimeout(() => {
        modalContent.classList.remove('opacity-0', 'scale-95');
        modalContent.classList.add('opacity-100', 'scale-100');
      }, 50);
  }

  function hideModal() {
      const modal = document.getElementById('crudModal');
      const modalContent = document.getElementById('crudModalContent');

      modalContent.classList.remove('opacity-100', 'scale-100');
      modalContent.classList.add('opacity-0', 'scale-95');

      setTimeout(() => {
        modal.classList.add('hidden');
      }, 150);
  }
  function addNewProduct() {
    fetch("{% url 'main:create_product_ajax' %}", {
      method: "POST",
      body: new FormData(document.querySelector('#productEntryForm')),
    })
    .then(response => refreshProduct())

    document.getElementById("productEntryForm").reset();
    document.querySelector("[data-modal-toggle='crudModal']").click();

    return false;
  }

  document.getElementById("submitProduct").onclick = addNewProduct
  document.getElementById("cancelButton").addEventListener("click", hideModal);
  document.getElementById("closeModalBtn").addEventListener("click", hideModal);

</script>

...
```
