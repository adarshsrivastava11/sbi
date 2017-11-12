# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PIL import Image
from django.shortcuts import render
from main.models import *
import requests
from django.http import *
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import cv2
# Functions to load and pre-process the images:
# Functions to load the CNN model
import signet
from cnn_model import CNNModel


model_weight_path = 'models/signet.pkl'
model = CNNModel(signet, model_weight_path)
# Functions for plotting:
print "server started"

# Create your views here.
@csrf_exempt
def create_acc(request):
    if request.method == 'POST':
        print request.POST
        try:
            acc_no = request.POST['acc_no']
            sig = request.FILES.get('signature')
        except ValueError:
            return HttpResponseForbidden('Malformed xml form')
        print acc_no
        url = "http://apiplatformcloudse-gseapicssbisecond-uqlpluu8.srv.ravcloud.com:8001/DigitalSignCreate"
        headers = {
                'team_id': "4916519817",
                'account_no': acc_no,
                'name': "Adarsh22",
                'mime_type': "image/jpeg",
                'api-key': "c0716b7d-c9f2-4587-bebc-b7daf71aafbc",
                }
        response = requests.request("POST", url, headers=headers,data=sig.read()) 
        a = Account(acc_no = acc_no, created = True)
        a.save()
        try:
            pass
        except:
            pass
        return HttpResponse("Form accepted", )
    else:
        return HttpResponseForbidden("GET, PUT, HEAD, not allowed")

@csrf_exempt
def verify(request):
    if request.method == 'POST':
        print request.POST
        try:
            acc_no = request.POST['acc_no']
            sig = request.FILES.get('signature')
        except ValueError:
            return HttpResponseForbidden('Malformed xml form')
        print acc_no
        url = "http://apiplatformcloudse-gseapicssbisecond-uqlpluu8.srv.ravcloud.com:8001/DigitalSignInfo/"+acc_no
        url = url + "/SIGNATURE/"
        headers = {
                'team_id': "4916519817",
                'account_no': acc_no,
                'name': "Adarsh22",
                'mime_type': "image/jpeg",
                'api-key': "c0716b7d-c9f2-4587-bebc-b7daf71aafbc",
                }
        response = requests.request("GET", url, headers=headers)
        fu = 'user_data/'+acc_no+'U.jpg'
        fd = 'user_data/'+acc_no+'D.jpg'
        with open('user_data/'+acc_no+'U.jpg', 'wb') as f:
            f.write(sig.read())
        with open('user_data/'+acc_no+'D.jpg', 'wb') as f:
            f.write(response.content)
        a = Account(acc_no = acc_no, created = True)
        a.save()
        img = Image.open(fu).convert('LA')
        img.save(fu)
        user1_sigs  = [cv2.imread(fu,0)]
        user2_sigs  = [cv2.imread(fd,0)]
        canvas_size = (952, 1360)
        processed_user1_sigs = np.array([preprocess_signature(sig, canvas_size) for sig in user1_sigs])
        processed_user2_sigs = np.array([preprocess_signature(sig, canvas_size) for sig in user2_sigs])
        user1_features = model.get_feature_vector_multiple(processed_user1_sigs, layer='fc2')
        user2_features = model.get_feature_vector_multiple(processed_user2_sigs, layer='fc2')
        try:
            pass
        except:
            pass
        return HttpResponse("Form accepted", )
    else:
        return HttpResponseForbidden("GET, PUT, HEAD, not allowed")
