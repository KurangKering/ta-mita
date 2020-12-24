from django.db import models
from django_pandas.managers import DataFrameManager
# Create your models here.
import json

class Dataset(models.Model):
	age = models.IntegerField(null=True, blank=True)
	sex = models.FloatField(null=True, blank=True)
	steroid = models.FloatField(null=True, blank=True)
	antivirals = models.FloatField(null=True, blank=True)
	fatigue = models.FloatField(null=True, blank=True)
	malaise = models.FloatField(null=True, blank=True)
	anorexia = models.FloatField(null=True, blank=True)
	liver_big = models.FloatField(null=True, blank=True)
	liver_firm = models.FloatField(null=True, blank=True)
	spleen_palpable = models.FloatField(null=True, blank=True)
	spiders = models.FloatField(null=True, blank=True)
	ascites = models.FloatField(null=True, blank=True)
	varices = models.FloatField(null=True, blank=True)
	bilirubin = models.FloatField(null=True, blank=True)
	alk_posphate = models.FloatField(null=True, blank=True)
	sgot = models.FloatField(null=True, blank=True)
	albumin = models.FloatField(null=True, blank=True)
	protime = models.FloatField(null=True, blank=True)
	histology = models.FloatField(null=True, blank=True)
	kelas = models.IntegerField(null=True, blank=True)


class DatasetPreprocessing(models.Model):
	age = models.FloatField(null=True, blank=True)
	sex = models.FloatField(null=True, blank=True)
	steroid = models.FloatField(null=True, blank=True)
	antivirals = models.FloatField(null=True, blank=True)
	fatigue = models.FloatField(null=True, blank=True)
	malaise = models.FloatField(null=True, blank=True)
	anorexia = models.FloatField(null=True, blank=True)
	liver_big = models.FloatField(null=True, blank=True)
	liver_firm = models.FloatField(null=True, blank=True)
	spleen_palpable = models.FloatField(null=True, blank=True)
	spiders = models.FloatField(null=True, blank=True)
	ascites = models.FloatField(null=True, blank=True)
	varices = models.FloatField(null=True, blank=True)
	bilirubin = models.FloatField(null=True, blank=True)
	alk_posphate = models.FloatField(null=True, blank=True)
	sgot = models.FloatField(null=True, blank=True)
	albumin = models.FloatField(null=True, blank=True)
	protime = models.FloatField(null=True, blank=True)
	histology = models.FloatField(null=True, blank=True)
	kelas = models.FloatField(null=True, blank=True)


