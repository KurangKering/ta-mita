from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
from sklearn.model_selection import train_test_split
import json
import os
from os.path import join
from django.conf import settings
import pandas as pd
from .models import Dataset, DatasetPreprocessing
from django.db import connection
from .libraries.preprocessing import normalisasi
# Create your views here.
np.random.seed(0)


def index(request):
    return render(request, 'backend/lvq/index.html')


def data_master(request):

    return render(request, 'backend/lvq/data_master.html')


def json_data_master(request):

    dataset = list(Dataset.objects.all().values())
    context = {
        "dataset": dataset
    }
    return JsonResponse(context, safe=False)


def tambah_data_master(request):
    return render(request, 'backend/lvq/tambah_data_master.html')


def proses_tambah_data_master(request):
    QueryDict = request.POST
    age = QueryDict.get('input-manual-age')
    sex = QueryDict.get('input-manual-sex')
    steroid = QueryDict.get('input-manual-steroid')
    antivirals = QueryDict.get('input-manual-antivirals')
    fatigue = QueryDict.get('input-manual-fatigue')
    malaise = QueryDict.get('input-manual-malaise')
    anorexia = QueryDict.get('input-manual-anorexia')
    liver_big = QueryDict.get('input-manual-liver_big')
    liver_firm = QueryDict.get('input-manual-liver_firm')
    spleen_palpable = QueryDict.get('input-manual-spleen_palpable')
    spiders = QueryDict.get('input-manual-spiders')
    ascites = QueryDict.get('input-manual-ascites')
    varices = QueryDict.get('input-manual-varices')
    bilirubin = QueryDict.get('input-manual-bilirubin')
    alk_posphate = QueryDict.get('input-manual-alk_posphate')
    sgot = QueryDict.get('input-manual-sgot')
    albumin = QueryDict.get('input-manual-albumin')
    protime = QueryDict.get('input-manual-protime')
    histology = QueryDict.get('input-manual-histology')
    kelas = QueryDict.get('input-manual-kelas')

    dataset = Dataset()
    dataset.age = age
    dataset.sex = sex
    dataset.steroid = steroid
    dataset.antivirals = antivirals
    dataset.fatigue = fatigue
    dataset.malaise = malaise
    dataset.anorexia = anorexia
    dataset.liver_big = liver_big
    dataset.liver_firm = liver_firm
    dataset.spleen_palpable = spleen_palpable
    dataset.spiders = spiders
    dataset.ascites = ascites
    dataset.varices = varices
    dataset.bilirubin = bilirubin
    dataset.alk_posphate = alk_posphate
    dataset.sgot = sgot
    dataset.albumin = albumin
    dataset.protime = protime
    dataset.histology = histology
    dataset.kelas = kelas
    dataset.save()

    success = 1
    context = {
        'success': success,
    }
    return JsonResponse(context, safe=False)

def edit_data_master(request, id_data=None):

    data = None
    if id_data is not None: 
        data = Dataset.objects.get(pk=id_data)

    context = {
        'data': data
    }

    return render(request, 'backend/lvq/edit_data_master.html', context)

def proses_edit_data_master(request):
    QueryDict = request.POST
    context = {
        'success': 1
    }

    return JsonResponse(context, safe=False)


def proses_hapus_data_master(request):
    Dataset.objects.all().delete()
    table_name = Dataset.objects.model._meta.db_table

    sql = "DELETE FROM SQLite_sequence WHERE name='{}';".format(table_name)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()

    success = 1
    context = {
        'success': success
    }

    return JsonResponse(context, safe=False)


def preprocessing(request):
    dataset_preprocessing = DatasetPreprocessing.objects.all()
    context = {
        'dataset': dataset_preprocessing
    }

    return render(request, 'backend/lvq/preprocessing.html', context)

def proses_hapus_data_preprocessing(request):

    DatasetPreprocessing.objects.all().delete()
    table_name = DatasetPreprocessing.objects.model._meta.db_table

    sql = "DELETE FROM SQLite_sequence WHERE name='{}';".format(table_name)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()

    success = 1
    context = {
        'success': success
    }

    return JsonResponse(context, safe=False)


def proses_preprocessing(request):
    dataset = Dataset.objects.all()
    df = pd.DataFrame(list(dataset.values()))
    df_normalisasi = normalisasi(df)

    model_instances = [DatasetPreprocessing(age=dataset.age,
                                            sex=dataset.sex,
                                            steroid=dataset.steroid,
                                            antivirals=dataset.antivirals,
                                            fatigue=dataset.fatigue,
                                            malaise=dataset.malaise,
                                            anorexia=dataset.anorexia,
                                            liver_big=dataset.liver_big,
                                            liver_firm=dataset.liver_firm,
                                            spleen_palpable=dataset.spleen_palpable,
                                            spiders=dataset.spiders,
                                            ascites=dataset.ascites,
                                            varices=dataset.varices,
                                            bilirubin=dataset.bilirubin,
                                            alk_posphate=dataset.alk_posphate,
                                            sgot=dataset.sgot,
                                            albumin=dataset.albumin,
                                            protime=dataset.protime,
                                            histology=dataset.histology,
                                            kelas=dataset.kelas, ) for dataset in df_normalisasi.itertuples()]

    DatasetPreprocessing.objects.bulk_create(model_instances)

    df_preprocessing = json.loads(df_normalisasi.to_json(orient="records"))

    success = 1
    context = {
        "df_preprocessing": df_preprocessing,
        'success': success
    }
    return JsonResponse(context, safe=False)


def json_data_preprocessing(request):
    dataset = list(DatasetPreprocessing.objects.all().values())
    context = {
        "dataset": dataset
    }

    return JsonResponse(context, safe=False)

def perbandingan_lvq(request):
    dataset = DatasetPreprocessing.objects.all()
    total_seluruh_data = dataset.count()
    context = {
        'total_seluruh_data': total_seluruh_data,

    }
    return render(request, 'backend/lvq/perbandingan_lvq.html', context)

def proses_perbandingan_lvq(request):
    QueryDict = request.POST 
    input_epochs = int(QueryDict.get('input-epochs'))
    input_data_uji = int(QueryDict.get('input-data_uji')) / 100
    input_learning_rate = float(QueryDict.get('input-learning_rate'))

    dataset = DatasetPreprocessing.objects.all()
    df_dataset = pd.DataFrame(list(dataset.values()))
    df_dataset['kelas'] = df_dataset['kelas'].astype(int)
    X = df_dataset.loc[:, ~df_dataset.columns.isin(['id', 'kelas'])]
    y = df_dataset.loc[:, df_dataset.columns.isin(['kelas'])]
    X_train, X_test, y_train, y_test = train_test_split( 
        X, y, test_size=float(input_data_uji), stratify=y, random_state=0)
    
    X_train = X_train.sort_index()
    X_test = X_test.sort_index()
    y_train = y_train.sort_index()
    y_test = y_test.sort_index()


    trained_lvq2 = proses_pelatihan_lvq2(X, y, X_train, y_train, 
        input_epochs, input_data_uji, input_learning_rate)

    trained_lvq21 = proses_pelatihan_lvq21(X, y, X_train, y_train, 
        input_epochs, input_data_uji, input_learning_rate)

    hasil_prediksi_lvq2 = trained_lvq2.predict(X_test)
    hasil_prediksi_lvq21 = trained_lvq21.predict(X_test)

    df_data_latih = df_dataset.iloc[X_train.index].copy()
    df_data_uji = df_dataset.iloc[X_test.index].copy()


    table_hasil_lvq = pd.DataFrame(columns=['id', 'kelas', 'hasil_lvq2', 'hasil_lvq21'])
    table_hasil_lvq['id'] = df_data_uji['id']
    table_hasil_lvq['kelas'] = df_data_uji['kelas']
    table_hasil_lvq['hasil_lvq2'] = hasil_prediksi_lvq2
    table_hasil_lvq['hasil_lvq21'] = hasil_prediksi_lvq21


    data_latih_context = json.loads(df_data_latih.to_json(orient="records"))
    data_uji_context = json.loads(df_data_uji.to_json(orient="records"))
    table_hasil_lvq_context = json.loads(table_hasil_lvq.to_json(orient="records"))

    kelas_data_uji_array = y_test.values.ravel().tolist()
    kelas_hasil_prediksi_lvq2 = hasil_prediksi_lvq2.tolist()
    kelas_hasil_prediksi_lvq21 = hasil_prediksi_lvq21.tolist()

    total_data_uji = len(y_test.index)
    total_benar_lvq2 =  int((y_test.values.ravel() == hasil_prediksi_lvq2).sum())
    total_benar_lvq21 = int((y_test.values.ravel() == hasil_prediksi_lvq21).sum())

    akurasi_lvq2 = float(total_benar_lvq2 /  total_data_uji) * 100
    akurasi_lvq21 = float(total_benar_lvq21 /  total_data_uji) * 100

    context = {
        'data_latih': data_latih_context,
        'data_uji': data_uji_context,
        'table_hasil_lvq': table_hasil_lvq_context,
        'epochs': input_epochs,
        'learning_rate': input_learning_rate,
        'jumlah_persen_data_uji': input_data_uji,
        'total_data_uji': total_data_uji,
        'total_benar_lvq2': total_benar_lvq2,
        'total_benar_lvq21': total_benar_lvq21,
        'akurasi_lvq2': akurasi_lvq2,
        'akurasi_lvq21': akurasi_lvq21,
        'kelas_data_uji_array': kelas_data_uji_array,
        'kelas_hasil_prediksi_lvq2': kelas_hasil_prediksi_lvq2,
        'kelas_hasil_prediksi_lvq21': kelas_hasil_prediksi_lvq21,
    }
    return JsonResponse(context, safe=False)

    
def proses_pelatihan_lvq2(X, y, X_train, y_train, epochs, data_uji, learning_rate):

    np.random.seed(0)
    from neupy import algorithms
    lvqnet2 = algorithms.LVQ2(
        n_inputs=X.shape[1], n_classes=np.unique(y).size, verbose=False, step=learning_rate)
    lvqnet2.train(X_train, y_train, epochs=int(epochs))
    return lvqnet2


def proses_pelatihan_lvq21(X, y, X_train, y_train, epochs, data_uji, learning_rate):
    
    np.random.seed(0)
    from neupy import algorithms
    lvqnet21 = algorithms.LVQ21(n_inputs=X.shape[1], n_classes=np.unique(y).size, 
        verbose=False, step=learning_rate)
    lvqnet21.train(X_train, y_train, epochs=int(epochs))
    return lvqnet21 