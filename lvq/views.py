from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, Http404
import numpy as np
from pprint import pprint
import json
import os
from os.path import join
from django.conf import settings
import pandas as pd
from .models import Dataset, DatasetPreprocessing
from django.db import connection
from .libraries.preprocessing import normalisasi
# Create your views here.

def index(request):
    return render(request, 'backend/lvq/index.html')

def data_master(request):
	dataset = Dataset.objects.all()
	context = {
		'dataset' : dataset
	}
	print(context)
	return render(request, 'backend/lvq/data_master.html', context)

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

def preprocessing(request):
	dataset_preprocessing = DatasetPreprocessing.objects.all()
	context = {
		'dataset': dataset_preprocessing
	}

	return render(request, 'backend/lvq/preprocessing.html', context);

def proses_hapus_data_preprocessing(request):

	DatasetPreprocessing.objects.all().delete();
	table_name = DatasetPreprocessing.objects.model._meta.db_table

	sql = "DELETE FROM SQLite_sequence WHERE name='{}';".format(table_name)
	with connection.cursor() as cursor:
		cursor.execute(sql)
		row = cursor.fetchone()



	success = 1
	context = {
		'success': success
	}

	return JsonResponse(context,safe=False)


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
		"dataset": dataset_preprocessing
	}

	return JsonResponse(context, safe=False)

def pelatihan(request):

	return render(request, 'backend/lvq/pelatihan.html')
