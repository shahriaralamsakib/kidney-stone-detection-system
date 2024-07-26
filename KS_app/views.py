from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from .forms import UserRegistration
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
import joblib
from .forms import ImageUploadForm
from PIL import Image
import cv2
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from django.core.files.storage import FileSystemStorage
from io import BytesIO
import numpy as np

# Create your views here.

def home(request):
    return render(request, 'home.html')

class UserRegistrationView(View):
        def get(self,request):
            form = UserRegistration()
            return render(request, 'registration.html', {'form':form})

        def post(self,request):
            form = UserRegistration(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/accounts/login/')
            return render(request, 'registration.html', {'form':form})


def success(request):
    return render(request, 'home/success.html')

def profile(request):
 return render(request, 'profile.html')

def image_upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():

            uploaded_image = form.cleaned_data['image']

            # Perform ML model prediction here
            input_image = np.array(preprocess_input_image(uploaded_image))
            input_image_reshape = input_image.reshape(1, 224, 224, 3)

            pred = get_output(input_image_reshape)  # Replace with your ML model prediction
            input_pred = np.argmax(pred, 1)
            output=''
            if input_pred[0] == 0:
                output = 'result0'
            else:
                output = 'result1'

            return redirect('output',output)
    else:
        form = ImageUploadForm()
    return render(request, 'prediction.html', {'form': form})

def logout_form(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

def output(request, rs):
    result = ''
    if rs == 'result0':
        result = 0
    elif rs == 'result1':
        result = 1

    return render(request, "output.html",{'result':result})

def preprocess_input_image(image_path):
    img = np.asarray(Image.open(image_path).convert("RGB"))
    img = cv2.resize(img, (224, 224))
    img = np.array(img)
    return img

def load_model():
    model = keras.models.load_model('KS_app/KidneyStone_model.h5')
    return model

def get_output(input_data):
    model = load_model()
    prediction = model.predict(input_data)
    return prediction

