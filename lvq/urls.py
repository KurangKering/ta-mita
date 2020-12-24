from django.urls import path

from . import views

urlpatterns = [
    path('data_master', views.data_master, name='lvq/data_master'),
    path('tambah_data_master', views.tambah_data_master, name='lvq/tambah_data_master'),
    path('proses_tambah_data_master', views.proses_tambah_data_master, name='lvq/proses_tambah_data_master'),
    path('preprocessing', views.preprocessing, name='lvq/preprocessing'),
    path('proses_preprocessing', views.proses_preprocessing, name='lvq/proses_preprocessing'),
    path('proses_hapus_data_preprocessing', views.proses_hapus_data_preprocessing, name='lvq/proses_hapus_data_preprocessing'),
    path('json_data_preprocessing', views.json_data_preprocessing, name='lvq/json_data_preprocessing'),
    path('pelatihan', views.pelatihan, name='lvq/pelatihan'),
]
