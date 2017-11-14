# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PIL import Image
from django.shortcuts import render
from backend.models import *
import requests
from django.http import *
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import cv2
# Functions to load and pre-process the images:
# Functions to load the CNN model
import signet
from cnn_model import CNNModel
from preprocess.normalize import normalize_image, resize_image, crop_center, preprocess_signature
model_weight_path = 'models/signet.pkl'
model = CNNModel(signet, model_weight_path)
# Functions for plotting:
print "server started"

def index(request):
    return render(request, 'index.html')
# Create your views here.
@csrf_exempt
def create_acc(request):
    error = ""
    if request.method == 'POST':
        print request.POST
        try:
            acc_no = request.POST['acc_no']
            name = request.POST['username']
            sig = request.FILES.get('signature', False)
        except ValueError:
            return HttpResponseForbidden('Malformed xml form')
        print acc_no
        url = "http://apiplatformcloudse-gseapicssbisecond-uqlpluu8.srv.ravcloud.com:8001/DigitalSignCreate"
        headers = {
                'team_id': "4916519817",
                'account_no': acc_no,
                'name': name,
                'mime_type': "image/jpeg",
                'api-key': "c0716b7d-c9f2-4587-bebc-b7daf71aafbc",
                }
        response = requests.request("POST", url, headers=headers,data=sig) 
        code = response.status_code
        if (code == 500):
            error = "Image Size larger than 50Kb. Please reduce the size."
        a = Account(acc_no = acc_no, created = True)
        a.save()
        try:
            pass
        except:
            pass
        error = "Account Created Successfully"
        return render(request,'upload_success.html',{'error':error})
    else:
        return render (request,'create.html',{'error':error})

@csrf_exempt
def verify(request):
    score = 0
    inference = ""
    if request.method == 'POST':
        print request.POST
        try:
            acc_no = request.POST['acc_no']
            sig = request.FILES.get('signature',False)
        except ValueError:
            return HttpResponseForbidden('Malformed xml form')
        print acc_no
        url="http://apiplatformcloudse-gseapicssbisecond-uqlpluu8.srv.ravcloud.com:8001/DigitalSignInfo/4916519817/"+acc_no+"/SIGNATURE"
        headers = {
                'api-key': "c0716b7d-c9f2-4587-bebc-b7daf71aafbc",
                }
        response = requests.request("GET", url, headers=headers)
        print sig
        fu = 'backend/static/'+acc_no+'U.png'
        imgU = acc_no+'U.png'
        fd = 'backend/static/'+acc_no+'D.png'
        imgD = acc_no+'D.png'
        img = Image.open(sig).convert('LA')
        img.save(fu)
        # f = open(fu, 'w')
        # f.write(sig.read())
        f = open(fd, 'w')
        f.write(response.content)
        f.close()

        img = Image.open(fd).convert('LA')
        img.save(fd)
        # f = open(fd, 'r')
        # print f
        print cv2.imread(fd,0)
        user1_sigs  = [cv2.imread(fu,0)]
        user2_sigs  = [cv2.imread(fd,0)]
        print user1_sigs
        print user2_sigs
        canvas_size = (952, 1360)
        processed_user1_sigs = np.array([preprocess_signature(sig, canvas_size) for sig in user1_sigs])
        processed_user2_sigs = np.array([preprocess_signature(sig, canvas_size) for sig in user2_sigs])
        user1_features = model.get_feature_vector_multiple(processed_user1_sigs, layer='fc2')
        user2_features = model.get_feature_vector_multiple(processed_user2_sigs, layer='fc2')
        print('Euclidean distance between signatures from the same user')
        score = 100-np.linalg.norm(user1_features[0] - user2_features[0])
        if (score > 85):
            inference = "Signature Belong to Same Person"
        if (score < 85 and score > 75):
            inference = "Possible Fake"
        else:
            inference = "Signatures Belong to Different Users"
        try:
            pass
        except:
            pass
        return render(request,'result.html',{'score':score,'result':inference,'fu':imgU,'fd':imgD})
    else:
        return render(request,'verify.html')
def testing(request):
    dists = []
    user1_sigs  = [cv2.imread('temp_data/m%d-min.jpg' % i,0) for i in  [1,2]]
    user2_sigs  = [cv2.imread('temp_data/s%d-min.jpg' % i,0) for i in  [2,3]]
    canvas_size = (952, 1360)
    processed_user1_sigs = np.array([preprocess_signature(sig, canvas_size) for sig in user1_sigs])
    processed_user2_sigs = np.array([preprocess_signature(sig, canvas_size) for sig in user2_sigs])
    user1_features = model.get_feature_vector_multiple(processed_user1_sigs, layer='fc2')
    user2_features = model.get_feature_vector_multiple(processed_user2_sigs, layer='fc2')
    diffSameUser = str(100.00-np.linalg.norm(user1_features[0] - user1_features[1]))
    diffFraud = str(100.00-np.linalg.norm(user1_features[0] - user2_features[0]))
    diffDifferentUser = str(100.00-np.linalg.norm(user1_features[0] - user2_features[1]))
    print(np.linalg.norm(user1_features[0] - user1_features[1]))
    print(np.linalg.norm(user1_features[0] - user2_features[0]))
    print(np.linalg.norm(user1_features[0] - user2_features[1]))
    for u2 in user2_features:
        for u1 in user1_features:
            dists.append(np.linalg.norm(u2-u1))
    # dists = [np.linalg.norm(u1 - u2) for u1 in user1_features for u2 in user2_features]
    print(dists)
    return render(request, 'test.html',{'sameUser':diffSameUser,'fraud':diffFraud, 'differentUser':diffDifferentUser})