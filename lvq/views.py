from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
from sklearn.model_selection import train_test_split
import json
import os
from os.path import join
from django.conf import settings
import pandas as pd
from .models import Dataset, DatasetPreprocessing, Inisialisasi, BobotAwal, BobotAkhir
from django.db import connection
from .libraries.preprocessing import normalisasi
from django.views.decorators.csrf import csrf_exempt
from .libraries.lvq_factory import *
from .libraries.bobot_awal_generator import bobot_awal_generator
from copy import deepcopy
np.random.seed(0)

def index(request):
    return render(request, 'backend/lvq/index.html')


def inisialisasi_data_awal(request):

    parameters = Inisialisasi.objects.first()
    if parameters == None:
        parameters = {}
        parameters['epochs'] = ''
        parameters['persen_uji'] = ''
        parameters['lr'] = ''
        parameters['pengurangan_lr'] = '' 
        parameters['minimum_lr'] = ''
        parameters['window'] = ''

    context = {
        'parameters': parameters
    }
    return render(request, 'backend/lvq/data_awal.html', context)

def simpan_inisialisasi(request):
    QueryDict = request.POST
    epochs = QueryDict.get('input-epochs')
    persen_uji = QueryDict.get('input-persen_uji')
    lr = QueryDict.get('input-lr')
    pengurangan_lr = QueryDict.get('input-pengurangan_lr')
    minimum_lr = QueryDict.get('input-minimum_lr')
    window = QueryDict.get('input-window')

    parameters = Inisialisasi.objects.first()
    if parameters == None:
        parameters = Inisialisasi()

    parameters.epochs = epochs
    parameters.persen_uji = persen_uji
    parameters.lr = lr
    parameters.pengurangan_lr = pengurangan_lr
    parameters.minimum_lr = minimum_lr
    parameters.window = window
    parameters.save()

    success = 1
    context = {
    'success': success,
    }
    return JsonResponse(context, safe=False)

def json_data_awal(request):

    dataset = list(Dataset.objects.all().values())
    context = {
        "dataset": dataset
    }
    return JsonResponse(context, safe=False)


def tambah_data_awal(request):
    return render(request, 'backend/lvq/tambah_data_awal.html')


def proses_tambah_data_awal(request):
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


@csrf_exempt
def proses_import_data_awal(request):
    raw_body = request.body.decode('utf-8')
    data_post = json.loads(raw_body)

    bulk_data = []
    for row in data_post:
        dataset = Dataset()
        dataset.age = float(row['AGE'])
        dataset.sex = float(row['SEX'])
        dataset.steroid = float(row['STEROID'])
        dataset.antivirals = float(row['ANTIVIRALS'])
        dataset.fatigue = float(row['FATIGUE'])
        dataset.malaise = float(row['MALAISE'])
        dataset.anorexia = float(row['ANOREXIA'])
        dataset.liver_big = float(row['LIVER BIG'])
        dataset.liver_firm = float(row['LIVER FIRM'])
        dataset.spleen_palpable = float(row['SPLEEN PALPABLE'])
        dataset.spiders = float(row['SPIDERS'])
        dataset.ascites = float(row['ASCITES'])
        dataset.varices = float(row['VARICES'])
        dataset.bilirubin = float(row['BILIRUBIN'])
        dataset.alk_posphate = float(row['ALK POSPHATE'])
        dataset.sgot = float(row['SGOT'])
        dataset.albumin = float(row['ALBUMIN'])
        dataset.protime = float(row['PROTIME'])
        dataset.histology = float(row['HISTOLOGY'])
        dataset.kelas = float(row['CLASS'])
        bulk_data.append(dataset)

    Dataset.objects.bulk_create(bulk_data)

    context = {
        'success': 1
    }
    return JsonResponse(context, safe=False);

def edit_data_awal(request, id_data=None):

    data = None
    if id_data is not None: 
        data = Dataset.objects.get(pk=id_data)

    context = {
        'data': data
    }

    return render(request, 'backend/lvq/edit_data_awal.html', context)

def proses_edit_data_awal(request):
    QueryDict = request.POST
    id_data_awal = QueryDict.get('input-manual-id_data_awal')
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

    dataset = Dataset.objects.get(pk=id_data_awal)
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



def proses_hapus_data_awal(request):
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


@csrf_exempt
def proses_hapus_satu_data_awal(request):
    QueryDict = request.POST
    id_data_awal = QueryDict.get('id_data_awal')

    data = Dataset.objects.get(pk=int(id_data_awal))

    data.delete()
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

    DatasetPreprocessing.objects.all().delete()
    table_name = DatasetPreprocessing.objects.model._meta.db_table

    sql = "DELETE FROM SQLite_sequence WHERE name='{}';".format(table_name)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()

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

def training_data(request):
    parameters = Inisialisasi.objects.first()
    bobot_awal = BobotAwal.objects.all()

    dataset = DatasetPreprocessing.objects.all()
    df_dataset = pd.DataFrame(list(dataset.values()))
    df_dataset['kelas'] = df_dataset['kelas'].astype(int)
    X = df_dataset.loc[:, ~df_dataset.columns.isin(['id', 'kelas'])]
    y = df_dataset.loc[:, df_dataset.columns.isin(['kelas'])]
    persen_uji = float(parameters.persen_uji) / 100
    X_train, X_test, y_train, y_test = train_test_split( 
        X, y, test_size=float(persen_uji), stratify=y, random_state=0)
    
    X_train = X_train.sort_index()
    X_test = X_test.sort_index()
    y_train = y_train.sort_index()
    y_test = y_test.sort_index()

    df_data_latih = df_dataset.iloc[X_train.index].copy()
    df_data_uji = df_dataset.iloc[X_test.index].copy()


    data_latih_context = json.loads(df_data_latih.to_json(orient="records"))
    data_uji_context = json.loads(df_data_uji.to_json(orient="records"))

    context = {
        'parameters': parameters,
        'bobot_awal': bobot_awal,
        'data_latih_context': data_latih_context,
        'data_uji_context': data_uji_context,
    }
    return render(request, 'backend/lvq/training_data.html', context)

def json_data_latih_uji(request):
    parameters = Inisialisasi.objects.first()
    dataset = DatasetPreprocessing.objects.all()
    df_dataset = pd.DataFrame(list(dataset.values()))
    df_dataset['kelas'] = df_dataset['kelas'].astype(int)
    X = df_dataset.loc[:, ~df_dataset.columns.isin(['id', 'kelas'])]
    y = df_dataset.loc[:, df_dataset.columns.isin(['kelas'])]
    persen_uji = float(parameters.persen_uji) / 100
    X_train, X_test, y_train, y_test = train_test_split( 
        X, y, test_size=float(persen_uji), stratify=y, random_state=0)
    
    X_train = X_train.sort_index()
    X_test = X_test.sort_index()
    y_train = y_train.sort_index()
    y_test = y_test.sort_index()

    df_data_latih = df_dataset.iloc[X_train.index].copy()
    df_data_uji = df_dataset.iloc[X_test.index].copy()


    data_latih_context = json.loads(df_data_latih.to_json(orient="records"))
    data_uji_context = json.loads(df_data_uji.to_json(orient="records"))

    context = {
        'data_latih_context': data_latih_context,
        'data_uji_context': data_uji_context,
    }
    return JsonResponse(context, safe=False)

def generate_bobot_awal(request):
    parameters = Inisialisasi.objects.first()
    dataset = DatasetPreprocessing.objects.all()
    df_dataset = pd.DataFrame(list(dataset.values()))
    df_dataset['kelas'] = df_dataset['kelas'].astype(int)
    X = df_dataset.loc[:, ~df_dataset.columns.isin(['id', 'kelas'])]
    y = df_dataset.loc[:, df_dataset.columns.isin(['kelas'])]
    persen_uji = float(parameters.persen_uji) / 100
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=float(persen_uji), stratify=y, random_state=0)

    X_train = X_train.sort_index()
    y_train = y_train.sort_index()
    
    index_bobot, data_bobot = bobot_awal_generator(X_train, y_train)

    df_bobot = df_dataset.iloc[X_train.iloc[index_bobot].index]

    BobotAwal.objects.all().delete()
    for x in range(len(index_bobot)):
        bobot = df_bobot.iloc[x]
        bobot_awal = BobotAwal()
        bobot_awal.dataset_id = bobot['id']
        bobot_awal.x1 = bobot['age']
        bobot_awal.x2 = bobot['sex']
        bobot_awal.x3 = bobot['steroid']
        bobot_awal.x4 = bobot['antivirals']
        bobot_awal.x5 = bobot['fatigue']
        bobot_awal.x6 = bobot['malaise']
        bobot_awal.x7 = bobot['anorexia']
        bobot_awal.x8 = bobot['liver_big']
        bobot_awal.x9 = bobot['liver_firm']
        bobot_awal.x10 = bobot['spleen_palpable']
        bobot_awal.x11 = bobot['spiders']
        bobot_awal.x12 = bobot['ascites']
        bobot_awal.x13 = bobot['varices']
        bobot_awal.x14 = bobot['bilirubin']
        bobot_awal.x15 = bobot['alk_posphate']
        bobot_awal.x16 = bobot['sgot']
        bobot_awal.x17 = bobot['albumin']
        bobot_awal.x18 = bobot['protime']
        bobot_awal.x19 = bobot['histology']
        bobot_awal.kelas = bobot['kelas']
        bobot_awal.save()
    
    bobot_awal = json.loads(df_bobot.to_json(orient="records"))

    context = {
        'success': 1,
        'bobot_awal': bobot_awal
    }
    return JsonResponse(context, safe=False)


def json_bobot_awal(requset):

    bobot_awal = BobotAwal.objects.all()
    bobot_awal_pd = pd.DataFrame(list(bobot_awal.values()))
    bobot_awal = json.loads(bobot_awal_pd.to_json(orient="records"))


    context = {
        'bobot_awal': bobot_awal
    }

    return JsonResponse(context, safe=False)

def pelatihan_lvq(request):
    parameters = Inisialisasi.objects.first()
    input_epochs = parameters.epochs
    input_data_uji = parameters.persen_uji / 100
    input_learning_rate = parameters.lr
    input_window = parameters.window
    input_pengurangan_learning_rate = parameters.pengurangan_lr
    input_minimum_learning_rate = parameters.minimum_lr

    dataset = DatasetPreprocessing.objects.all()
    bobot_awal = BobotAwal.objects.all()

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

    bobot_awal_pd = pd.DataFrame(list(bobot_awal.values()))
    bobot_awal_array = bobot_awal_pd.loc[:, ~bobot_awal_pd.columns.isin(['id', 'dataset_id', 'kelas'])].copy().to_numpy()


    bobot_untuk_lvq2 = deepcopy(bobot_awal_array)
    trained_lvq2 = proses_pelatihan_lvq2(X, 
        y, 
        X_train, 
        y_train, 
        input_epochs, 
        step=input_learning_rate, 
        epsilon=input_window, 
        pengurangan_step=input_pengurangan_learning_rate, 
        minstep=input_minimum_learning_rate,
        weight=bobot_untuk_lvq2)

    bobot_untuk_lvq21 = deepcopy(bobot_awal_array)

    trained_lvq21 = proses_pelatihan_lvq21(X, 
        y, 
        X_train, 
        y_train, 
        input_epochs, 
        step=input_learning_rate, 
        epsilon=input_window, 
        pengurangan_step=input_pengurangan_learning_rate, 
        minstep=input_minimum_learning_rate,
        weight=bobot_untuk_lvq21)

    final_weight_lvq2 = trained_lvq2.weight.tolist()
    final_weight_lvq21 = trained_lvq21.weight.tolist()

    BobotAkhir.objects.all().delete()

    for x in range(len(final_weight_lvq2)):
        bobot_akhir_lvq2 = BobotAkhir()
        bobot_akhir_lvq2.x1 = final_weight_lvq2[x][0]
        bobot_akhir_lvq2.x2 = final_weight_lvq2[x][1]
        bobot_akhir_lvq2.x3 = final_weight_lvq2[x][2]
        bobot_akhir_lvq2.x4 = final_weight_lvq2[x][3]
        bobot_akhir_lvq2.x5 = final_weight_lvq2[x][4]
        bobot_akhir_lvq2.x6 = final_weight_lvq2[x][5]
        bobot_akhir_lvq2.x7 = final_weight_lvq2[x][6]
        bobot_akhir_lvq2.x8 = final_weight_lvq2[x][7]
        bobot_akhir_lvq2.x9 = final_weight_lvq2[x][8]
        bobot_akhir_lvq2.x10 = final_weight_lvq2[x][9]
        bobot_akhir_lvq2.x11 = final_weight_lvq2[x][10]
        bobot_akhir_lvq2.x12 = final_weight_lvq2[x][11]
        bobot_akhir_lvq2.x13 = final_weight_lvq2[x][12]
        bobot_akhir_lvq2.x14 = final_weight_lvq2[x][13]
        bobot_akhir_lvq2.x15 = final_weight_lvq2[x][14]
        bobot_akhir_lvq2.x16 = final_weight_lvq2[x][15]
        bobot_akhir_lvq2.x17 = final_weight_lvq2[x][16]
        bobot_akhir_lvq2.x18 = final_weight_lvq2[x][17]
        bobot_akhir_lvq2.x19 = final_weight_lvq2[x][18]
        bobot_akhir_lvq2.kelas = x
        bobot_akhir_lvq2.metode = "lvq2"
        bobot_akhir_lvq2.save()

    for x in range(len(final_weight_lvq21)):
        bobot_akhir_lvq21 = BobotAkhir()
        bobot_akhir_lvq21.x1 = final_weight_lvq21[x][0]
        bobot_akhir_lvq21.x2 = final_weight_lvq21[x][1]
        bobot_akhir_lvq21.x3 = final_weight_lvq21[x][2]
        bobot_akhir_lvq21.x4 = final_weight_lvq21[x][3]
        bobot_akhir_lvq21.x5 = final_weight_lvq21[x][4]
        bobot_akhir_lvq21.x6 = final_weight_lvq21[x][5]
        bobot_akhir_lvq21.x7 = final_weight_lvq21[x][6]
        bobot_akhir_lvq21.x8 = final_weight_lvq21[x][7]
        bobot_akhir_lvq21.x9 = final_weight_lvq21[x][8]
        bobot_akhir_lvq21.x10 = final_weight_lvq21[x][9]
        bobot_akhir_lvq21.x11 = final_weight_lvq21[x][10]
        bobot_akhir_lvq21.x12 = final_weight_lvq21[x][11]
        bobot_akhir_lvq21.x13 = final_weight_lvq21[x][12]
        bobot_akhir_lvq21.x14 = final_weight_lvq21[x][13]
        bobot_akhir_lvq21.x15 = final_weight_lvq21[x][14]
        bobot_akhir_lvq21.x16 = final_weight_lvq21[x][15]
        bobot_akhir_lvq21.x17 = final_weight_lvq21[x][16]
        bobot_akhir_lvq21.x18 = final_weight_lvq21[x][17]
        bobot_akhir_lvq21.x19 = final_weight_lvq21[x][18]
        bobot_akhir_lvq21.kelas = x
        bobot_akhir_lvq21.metode = "lvq21"
        bobot_akhir_lvq21.save()

    context = {
        'final_weight_lvq2': final_weight_lvq2,
        'final_weight_lvq21': final_weight_lvq21,


    }
    return JsonResponse(context, safe=False)

def pelatihan_lvq2(request):

    parameters = Inisialisasi.objects.first()
    input_epochs = parameters.epochs
    input_data_uji = parameters.persen_uji / 100
    input_learning_rate = parameters.lr
    input_window = parameters.window
    input_pengurangan_learning_rate = parameters.pengurangan_lr
    input_minimum_learning_rate = parameters.minimum_lr

    dataset = DatasetPreprocessing.objects.all()
    bobot_awal = BobotAwal.objects.all()

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

    bobot_awal_pd = pd.DataFrame(list(bobot_awal.values()))
    bobot_awal_array = bobot_awal_pd.loc[:, ~bobot_awal_pd.columns.isin(['id', 'dataset_id', 'kelas'])].copy().to_numpy()



    trained_lvq2 = proses_pelatihan_lvq2(X, 
        y, 
        X_train, 
        y_train, 
        input_epochs, 
        step=input_learning_rate, 
        epsilon=input_window, 
        pengurangan_step=input_pengurangan_learning_rate, 
        minstep=input_minimum_learning_rate,
        weight=bobot_awal_array)

    final_weight_lvq2 = trained_lvq2.weight.tolist()

    BobotAkhir.objects.filter(metode="lvq2").delete()

    for x in range(len(final_weight_lvq2)):
        bobot_akhir = BobotAkhir()
        bobot_akhir.x1 = final_weight_lvq2[x][0]
        bobot_akhir.x2 = final_weight_lvq2[x][1]
        bobot_akhir.x3 = final_weight_lvq2[x][2]
        bobot_akhir.x4 = final_weight_lvq2[x][3]
        bobot_akhir.x5 = final_weight_lvq2[x][4]
        bobot_akhir.x6 = final_weight_lvq2[x][5]
        bobot_akhir.x7 = final_weight_lvq2[x][6]
        bobot_akhir.x8 = final_weight_lvq2[x][7]
        bobot_akhir.x9 = final_weight_lvq2[x][8]
        bobot_akhir.x10 = final_weight_lvq2[x][9]
        bobot_akhir.x11 = final_weight_lvq2[x][10]
        bobot_akhir.x12 = final_weight_lvq2[x][11]
        bobot_akhir.x13 = final_weight_lvq2[x][12]
        bobot_akhir.x14 = final_weight_lvq2[x][13]
        bobot_akhir.x15 = final_weight_lvq2[x][14]
        bobot_akhir.x16 = final_weight_lvq2[x][15]
        bobot_akhir.x17 = final_weight_lvq2[x][16]
        bobot_akhir.x18 = final_weight_lvq2[x][17]
        bobot_akhir.x19 = final_weight_lvq2[x][18]
        bobot_akhir.kelas = x
        bobot_akhir.metode = "lvq2"
        bobot_akhir.save()

    context = {
        'final_weight_lvq2': final_weight_lvq2,


    }
    return JsonResponse(context, safe=False)

def pelatihan_lvq21(request):

    parameters = Inisialisasi.objects.first()
    input_epochs = parameters.epochs
    input_data_uji = parameters.persen_uji / 100
    input_learning_rate = parameters.lr
    input_window = parameters.window
    input_pengurangan_learning_rate = parameters.pengurangan_lr
    input_minimum_learning_rate = parameters.minimum_lr

    dataset = DatasetPreprocessing.objects.all()
    bobot_awal = BobotAwal.objects.all()

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

    bobot_awal_pd = pd.DataFrame(list(bobot_awal.values()))
    bobot_awal_array = bobot_awal_pd.loc[:, ~bobot_awal_pd.columns.isin(['id', 'dataset_id', 'kelas'])].copy().to_numpy()



    trained_lvq21 = proses_pelatihan_lvq21(X, 
        y, 
        X_train, 
        y_train, 
        input_epochs, 
        step=input_learning_rate, 
        epsilon=input_window, 
        pengurangan_step=input_pengurangan_learning_rate, 
        minstep=input_minimum_learning_rate,
        weight=bobot_awal_array)

    final_weight_lvq21 = trained_lvq21.weight.tolist()

    BobotAkhir.objects.filter(metode="lvq21").delete()

    for x in range(len(final_weight_lvq21)):
        bobot_akhir = BobotAkhir()
        bobot_akhir.x1 = final_weight_lvq21[x][0]
        bobot_akhir.x2 = final_weight_lvq21[x][1]
        bobot_akhir.x3 = final_weight_lvq21[x][2]
        bobot_akhir.x4 = final_weight_lvq21[x][3]
        bobot_akhir.x5 = final_weight_lvq21[x][4]
        bobot_akhir.x6 = final_weight_lvq21[x][5]
        bobot_akhir.x7 = final_weight_lvq21[x][6]
        bobot_akhir.x8 = final_weight_lvq21[x][7]
        bobot_akhir.x9 = final_weight_lvq21[x][8]
        bobot_akhir.x10 = final_weight_lvq21[x][9]
        bobot_akhir.x11 = final_weight_lvq21[x][10]
        bobot_akhir.x12 = final_weight_lvq21[x][11]
        bobot_akhir.x13 = final_weight_lvq21[x][12]
        bobot_akhir.x14 = final_weight_lvq21[x][13]
        bobot_akhir.x15 = final_weight_lvq21[x][14]
        bobot_akhir.x16 = final_weight_lvq21[x][15]
        bobot_akhir.x17 = final_weight_lvq21[x][16]
        bobot_akhir.x18 = final_weight_lvq21[x][17]
        bobot_akhir.x19 = final_weight_lvq21[x][18]
        bobot_akhir.kelas = x
        bobot_akhir.metode = "lvq21"
        bobot_akhir.save()

    context = {
        'final_weight_lvq21': final_weight_lvq21,


    }
    return JsonResponse(context, safe=False)

def generate_data_uji(request):
    parameters = Inisialisasi.objects.first()
    input_data_uji = parameters.persen_uji / 100
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

    df_data_uji = df_dataset.iloc[X_test.index].copy()


    data_uji_context = json.loads(df_data_uji.to_json(orient="records"))

    context = {
        'data_uji': data_uji_context,
    }

    return JsonResponse(context, safe=False)


def generate_bobot_akhir(request):
    QueryDict = request.POST
    metode = QueryDict.get('metode')

    bobot_akhir = BobotAkhir.objects.filter(metode=metode)
    bobot_akhir_pd = pd.DataFrame(list(bobot_akhir.values()))
    bobot_akhir_array = bobot_akhir_pd.loc[:, ~bobot_akhir_pd.columns.isin(['id', 'kelas', 'metode'])].copy().to_numpy()

    context = {
        'bobot_akhir': bobot_akhir_array.tolist()
    }

    return JsonResponse(context, safe=False)


def testing_data(request):
    parameters = Inisialisasi.objects.first()
    input_data_uji = parameters.persen_uji / 100
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

    bobot_akhir_lvq2 = BobotAkhir.objects.filter(metode="lvq2")
    bobot_akhir_lvq2_pd = pd.DataFrame(list(bobot_akhir_lvq2.values()))
    bobot_akhir_lvq2_array = bobot_akhir_lvq2_pd.loc[:, ~bobot_akhir_lvq2_pd.columns.isin(['id', 'kelas', 'metode'])].copy().to_numpy()

    bobot_akhir_lvq21 = BobotAkhir.objects.filter(metode="lvq21")
    bobot_akhir_lvq21_pd = pd.DataFrame(list(bobot_akhir_lvq21.values()))
    bobot_akhir_lvq21_array = bobot_akhir_lvq21_pd.loc[:, ~bobot_akhir_lvq21_pd.columns.isin(['id', 'kelas', 'metode'])].copy().to_numpy()


    df_data_uji = df_dataset.iloc[X_test.index].copy()


    data_uji_context = json.loads(df_data_uji.to_json(orient="records"))

    context = {
        'data_uji': data_uji_context,
        'final_weight_lvq2': bobot_akhir_lvq2_array.tolist(),
        'final_weight_lvq21': bobot_akhir_lvq21_array.tolist(),
    }
    return render(request, 'backend/lvq/testing_data.html', context)

def testing_data_lvq2(request):
    parameters = Inisialisasi.objects.first()

    input_epochs = parameters.epochs
    input_data_uji = parameters.persen_uji / 100
    input_learning_rate = parameters.lr
    input_window = parameters.window
    input_pengurangan_learning_rate = parameters.pengurangan_lr
    input_minimum_learning_rate = parameters.minimum_lr

    dataset = DatasetPreprocessing.objects.all()

    bobot_akhir = BobotAkhir.objects.filter(metode="lvq2")
    bobot_akhir_pd = pd.DataFrame(list(bobot_akhir.values()))
    bobot_akhir_array = bobot_akhir_pd.loc[:, ~bobot_akhir_pd.columns.isin(['id', 'kelas', 'metode'])].copy().to_numpy()


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

    hasil_testing_lvq2 = proses_testing_lvq2(X, y, 
        X_test,
        weight=bobot_akhir_array,
        step=input_learning_rate, 
        epsilon=input_window, 
        pengurangan_step=input_pengurangan_learning_rate, 
        minstep=input_minimum_learning_rate)

    df_data_latih = df_dataset.iloc[X_train.index].copy()
    df_data_uji = df_dataset.iloc[X_test.index].copy()


    table_hasil_lvq = pd.DataFrame(columns=['id', 'kelas', 'hasil_lvq2'])
    table_hasil_lvq['id'] = df_data_uji['id']
    table_hasil_lvq['kelas'] = df_data_uji['kelas']
    table_hasil_lvq['hasil_lvq2'] = hasil_testing_lvq2


    data_latih_context = json.loads(df_data_latih.to_json(orient="records"))
    data_uji_context = json.loads(df_data_uji.to_json(orient="records"))
    table_hasil_lvq_context = json.loads(table_hasil_lvq.to_json(orient="records"))

    kelas_data_uji_array = y_test.values.ravel().tolist()
    kelas_hasil_prediksi_lvq2 = hasil_testing_lvq2.tolist()

    total_data_uji = len(y_test.index)
    total_benar_lvq2 =  int((y_test.values.ravel() == hasil_testing_lvq2).sum())

    akurasi_lvq2 = float(total_benar_lvq2 /  total_data_uji) * 100

    context = {
        'data_latih': data_latih_context,
        'data_uji': data_uji_context,
        'table_hasil_lvq': table_hasil_lvq_context,
        'epochs': input_epochs,
        'learning_rate': input_learning_rate,
        'jumlah_persen_data_uji': input_data_uji,
        'total_data_uji': total_data_uji,
        'total_benar_lvq2': total_benar_lvq2,
        'akurasi_lvq2': akurasi_lvq2,
        'kelas_data_uji_array': kelas_data_uji_array,
        'kelas_hasil_prediksi_lvq2': kelas_hasil_prediksi_lvq2,
        'final_weight_lvq2': bobot_akhir_array.tolist(),


    }
    return JsonResponse(context, safe=False)


def testing_data_lvq21(request):
    parameters = Inisialisasi.objects.first()

    input_epochs = parameters.epochs
    input_data_uji = parameters.persen_uji / 100
    input_learning_rate = parameters.lr
    input_window = parameters.window
    input_pengurangan_learning_rate = parameters.pengurangan_lr
    input_minimum_learning_rate = parameters.minimum_lr

    dataset = DatasetPreprocessing.objects.all()

    bobot_akhir = BobotAkhir.objects.filter(metode="lvq21")
    bobot_akhir_pd = pd.DataFrame(list(bobot_akhir.values()))
    bobot_akhir_array = bobot_akhir_pd.loc[:, ~bobot_akhir_pd.columns.isin(['id', 'kelas', 'metode'])].copy().to_numpy()


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

    hasil_testing_lvq21 = proses_testing_lvq21(X, y, 
        X_test,
        weight=bobot_akhir_array,
        step=input_learning_rate, 
        epsilon=input_window, 
        pengurangan_step=input_pengurangan_learning_rate, 
        minstep=input_minimum_learning_rate)

    df_data_latih = df_dataset.iloc[X_train.index].copy()
    df_data_uji = df_dataset.iloc[X_test.index].copy()


    table_hasil_lvq = pd.DataFrame(columns=['id', 'kelas', 'hasil_lvq21'])
    table_hasil_lvq['id'] = df_data_uji['id']
    table_hasil_lvq['kelas'] = df_data_uji['kelas']
    table_hasil_lvq['hasil_lvq21'] = hasil_testing_lvq21


    data_latih_context = json.loads(df_data_latih.to_json(orient="records"))
    data_uji_context = json.loads(df_data_uji.to_json(orient="records"))
    table_hasil_lvq_context = json.loads(table_hasil_lvq.to_json(orient="records"))

    kelas_data_uji_array = y_test.values.ravel().tolist()
    kelas_hasil_prediksi_lvq21 = hasil_testing_lvq21.tolist()

    total_data_uji = len(y_test.index)
    total_benar_lvq21 =  int((y_test.values.ravel() == hasil_testing_lvq21).sum())

    akurasi_lvq21 = float(total_benar_lvq21 /  total_data_uji) * 100

    context = {
        'data_latih': data_latih_context,
        'data_uji': data_uji_context,
        'table_hasil_lvq': table_hasil_lvq_context,
        'epochs': input_epochs,
        'learning_rate': input_learning_rate,
        'jumlah_persen_data_uji': input_data_uji,
        'total_data_uji': total_data_uji,
        'total_benar_lvq21': total_benar_lvq21,
        'akurasi_lvq21': akurasi_lvq21,
        'kelas_data_uji_array': kelas_data_uji_array,
        'kelas_hasil_prediksi_lvq21': kelas_hasil_prediksi_lvq21,
        'final_weight_lvq21': bobot_akhir_array.tolist(),


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
    input_window = float(QueryDict.get('input-window'))
    input_pengurangan_learning_rate = float(QueryDict.get('input-pengurangan_learning_rate'))
    input_minimum_learning_rate = float(QueryDict.get('input-minimum_learning_rate'))

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
        input_epochs, step=input_learning_rate, epsilon=input_window, pengurangan_step=input_pengurangan_learning_rate, minstep=input_minimum_learning_rate)

    trained_lvq21 = proses_pelatihan_lvq21(X, y, X_train, y_train, 
        input_epochs, step=input_learning_rate, epsilon=input_window,pengurangan_step=input_pengurangan_learning_rate, minstep=input_minimum_learning_rate)

    initial_weight_lvq2 = trained_lvq2.initial_weight.tolist()
    initial_weight_lvq21 = trained_lvq21.initial_weight.tolist()

    final_weight_lvq2 = trained_lvq2.weight.tolist()
    final_weight_lvq21 = trained_lvq21.weight.tolist()

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
        'initial_weight_lvq2': initial_weight_lvq2,
        'initial_weight_lvq21': initial_weight_lvq21,
        'final_weight_lvq2': final_weight_lvq2,
        'final_weight_lvq21': final_weight_lvq21,


    }
    return JsonResponse(context, safe=False)

    
def proses_testing_lvq(request):
    parameters = Inisialisasi.objects.first()

    input_epochs = int(request.GET.get('epochs', parameters.epochs))
    persen_uji = float(request.GET.get('persen_uji', parameters.persen_uji))
    input_data_uji = persen_uji / 100
    input_learning_rate = float(request.GET.get('lr', parameters.lr))
    input_window = float(request.GET.get('window', parameters.window))
    input_pengurangan_learning_rate = float(request.GET.get('pengurangan_lr', parameters.pengurangan_lr))
    input_minimum_learning_rate = float(request.GET.get('minimum_lr', parameters.minimum_lr))

    dataset = DatasetPreprocessing.objects.all()

    bobot_akhir_lvq2 = BobotAkhir.objects.filter(metode="lvq2")
    bobot_akhir_lvq2_pd = pd.DataFrame(list(bobot_akhir_lvq2.values()))
    bobot_akhir_lvq2_array = bobot_akhir_lvq2_pd.loc[:, ~bobot_akhir_lvq2_pd.columns.isin(['id', 'kelas', 'metode'])].copy().to_numpy()

    bobot_akhir_lvq21 = BobotAkhir.objects.filter(metode="lvq21")
    bobot_akhir_lvq21_pd = pd.DataFrame(list(bobot_akhir_lvq21.values()))
    bobot_akhir_lvq21_array = bobot_akhir_lvq21_pd.loc[:, ~bobot_akhir_lvq21_pd.columns.isin(['id', 'kelas', 'metode'])].copy().to_numpy()


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

    hasil_testing_lvq2 = proses_testing_lvq2(X, y, 
        X_test,
        weight=bobot_akhir_lvq2_array,
        step=input_learning_rate, 
        epsilon=input_window, 
        pengurangan_step=input_pengurangan_learning_rate, 
        minstep=input_minimum_learning_rate)

    hasil_testing_lvq21 = proses_testing_lvq21(X, y, 
        X_test,
        weight=bobot_akhir_lvq21_array,
        step=input_learning_rate, 
        epsilon=input_window, 
        pengurangan_step=input_pengurangan_learning_rate, 
        minstep=input_minimum_learning_rate)

    df_data_uji = df_dataset.iloc[X_test.index].copy()


    table_hasil_lvq = pd.DataFrame(columns=['id', 'kelas', 'hasil_lvq2', 'hasil_lvq21'])
    table_hasil_lvq['id'] = df_data_uji['id']
    table_hasil_lvq['kelas'] = df_data_uji['kelas']
    table_hasil_lvq['hasil_lvq2'] = hasil_testing_lvq2
    table_hasil_lvq['hasil_lvq21'] = hasil_testing_lvq21

    table_hasil_lvq_context = json.loads(table_hasil_lvq.to_json(orient="records"))

    kelas_data_uji_array = y_test.values.ravel().tolist()
    kelas_hasil_testing_lvq2 = hasil_testing_lvq2.tolist()
    kelas_hasil_testing_lvq21 = hasil_testing_lvq21.tolist()

    total_data_uji = len(y_test.index)
    total_benar_lvq2 =  int((y_test.values.ravel() == hasil_testing_lvq2).sum())
    total_benar_lvq21 = int((y_test.values.ravel() == hasil_testing_lvq21).sum())

    akurasi_lvq2 = float(total_benar_lvq2 /  total_data_uji) * 100
    akurasi_lvq21 = float(total_benar_lvq21 /  total_data_uji) * 100

    context = {
        'table_hasil_lvq': table_hasil_lvq_context,
        'epochs': input_epochs,
        'learning_rate': input_learning_rate,
        'jumlah_persen_data_uji': parameters.persen_uji,
        'total_data_uji': total_data_uji,
        'total_benar_lvq2': total_benar_lvq2,
        'total_benar_lvq21': total_benar_lvq21,
        'akurasi_lvq2': akurasi_lvq2,
        'akurasi_lvq21': akurasi_lvq21,
        'kelas_data_uji_array': kelas_data_uji_array,
        'kelas_hasil_testing_lvq2': kelas_hasil_testing_lvq2,
        'kelas_hasil_testing_lvq21': kelas_hasil_testing_lvq21,
    }
    return JsonResponse(context, safe=False)

    