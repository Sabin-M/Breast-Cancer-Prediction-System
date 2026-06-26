from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import numpy as np
import joblib
model = joblib.load('model.pkl')
le = joblib.load('label_encoder.pkl')
scaler = joblib.load('scaler.pkl')

# Login View

def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid Username or Password'
            })

    return render(request, 'login.html')

# Logout

def logout_view(request):
    logout(request)
    return redirect('login')

# Home Page

@login_required
def home(request):

    result = None

    if request.method == 'POST':

        data = [
            float(request.POST['radius_mean']),
            float(request.POST['texture_mean']),
            float(request.POST['perimeter_mean']),
            float(request.POST['area_mean']),
            float(request.POST['smoothness_mean']),
            float(request.POST['compactness_mean']),
            float(request.POST['concavity_mean']),
            float(request.POST['concave_points_mean']),
            float(request.POST['symmetry_mean']),
            float(request.POST['fractal_dimension_mean'])
        ]

        data = np.array(data).reshape(1, -1)

        scaled_data = scaler.transform(data)

        prediction = model.predict(scaled_data)

        result = le.inverse_transform(prediction)[0]

        if result == 'M':
            result = 'Malignant means Positive Cancer'
        else:
            result = 'Benign means Negative Cancer'

    return render(request, 'home.html', {
        'result': result
    })