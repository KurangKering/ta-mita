from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
import numpy as np
import json
import os
from os.path import join
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings


def index(request):
    return render(request, 'frontend/index.html')

def dashboard(request):
	return render(request, 'backend/dashboard.html')
