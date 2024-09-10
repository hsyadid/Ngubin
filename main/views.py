from django.shortcuts import render

# Create your views here.
def home(request):
    detail = {
        'nama_apps': 'Ngubin E-commerce',
        'nama_mahasiswa': 'Hubban Syadid',
        'kelas' : 'PBP-A',
    }

    return render(request, 'index.html', detail)
