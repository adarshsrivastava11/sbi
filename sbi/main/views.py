# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from main.models import *
import requests
from django.http import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def create_acc(request):
    if request.method == 'POST':
        print request.POST
        try:
            acc_no = request.POST['acc_no']
            #sig = request.FILES.get('signature')
        except ValueError:
            return HttpResponseForbidden('Malformed xml form')
        print acc_no
        a = Account(acc_no = acc_no, created = True)
        a.save()
        try:
            pass
        except:
            pass
        return HttpResponse("Form accepted", )
    else:
        return HttpResponseForbidden("GET, PUT, HEAD, not allowed")

