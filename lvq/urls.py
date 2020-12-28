from django.urls import path

from . import views

urlpatterns = [
    path('data_master', views.data_master, name='lvq/data_master'),
    path('tambah_data_master', views.tambah_data_master, name='lvq/tambah_data_master'),
    path('json_data_master', views.json_data_master, name='lvq/json_data_master'),
    path('proses_tambah_data_master', views.proses_tambah_data_master, name='lvq/proses_tambah_data_master'),
    path('proses_import_data_master', views.proses_import_data_master, name='lvq/proses_import_data_master'),
    path('edit_data_master/<id_data>', views.edit_data_master, name='lvq/edit_data_master'),
    path('proses_edit_data_master', views.proses_edit_data_master, name='lvq/proses_edit_data_master'),
    path('proses_hapus_data_master', views.proses_hapus_data_master, name='lvq/proses_hapus_data_master'),
    path('preprocessing', views.preprocessing, name='lvq/preprocessing'),
    path('proses_preprocessing', views.proses_preprocessing, name='lvq/proses_preprocessing'),
    path('proses_hapus_data_preprocessing', views.proses_hapus_data_preprocessing, name='lvq/proses_hapus_data_preprocessing'),
    path('json_data_preprocessing', views.json_data_preprocessing, name='lvq/json_data_preprocessing'),
    path('perbandingan_lvq', views.perbandingan_lvq, name='lvq/perbandingan_lvq'),
    path('proses_perbandingan_lvq', views.proses_perbandingan_lvq, name='lvq/proses_perbandingan_lvq'),
    path('proses_pelatihan_lvq2', views.proses_pelatihan_lvq2, name='lvq/proses_pelatihan_lvq2'),
    path('proses_pelatihan_lvq21', views.proses_pelatihan_lvq21, name='lvq/proses_pelatihan_lvq21'),
]
