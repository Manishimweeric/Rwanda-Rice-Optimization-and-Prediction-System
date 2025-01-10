# views.py
from pyexpat.errors import messages
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
import joblib
from django.contrib.auth.decorators import login_required
# List all roles (Read)
def role_list(request):
    roles = Role.objects.filter(is_active=True)
    return render(request, 'myapp/role_list.html', {'roles': roles})

# Create a new role (Create)
def role_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        is_active = request.POST.get('is_active') == 'on'
        Role.objects.create(name=name, is_active=is_active)
        return redirect('role_list')
    return render(request, 'myapp/role_create.html')

# Update an existing role (Update)
def role_update(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.name = request.POST.get('name')
        role.is_active = request.POST.get('is_active') == 'on'
        role.save()
        return redirect('role_list')
    return render(request, 'myapp/role_update.html', {'role': role})

# Delete a role (Delete)
def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.is_active = False  # Soft delete
        role.save()
        return redirect('role_list')
    return render(request, 'myapp/role_confirm_delete.html', {'role': role})

# Signup View
def signup(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Simple validation
        if password != confirm_password:
            return render(request, 'myapp/signup.html', {'error': 'Passwords do not match'})

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'myapp/signup.html', {'error': 'Email already registered'})

        # Create the user
        user = User(
            fullname=fullname,
            email=email,
            password=make_password(password),
            role=Role.objects.get(name='User')  # Default role
        )
        user.save()

        # Log the user in
        login(request, user)

        # Redirect to home page or another page
        return redirect('login')
    
    return render(request, 'myapp/signup.html')

# Login View
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'myapp/login.html', {'error': 'Invalid email or password'})

    return render(request, 'myapp/login.html')

def home(request):

    return render(request, 'myapp/index.html')


def admin_dashboard(request):
    
    return render(request, 'myapp/admin_dashboard.html')


model = joblib.load('D:\Project\Rwanda-Rice-Optimization-and-Prediction-System\Rwanda-Rice-Optimization-and-Prediction-System\myproject\myapp\yield_prediction_model.joblib')

@login_required
def make_prediction(request):
    if request.method == 'POST':
        # Collect form data directly from request.POST
        try:
            soil_ph = float(request.POST.get('soil_ph'))
            water_availability = float(request.POST.get('water_availability'))
            organic_matter = float(request.POST.get('organic_matter'))
            nitrogen = float(request.POST.get('nitrogen'))
            phosphorus = float(request.POST.get('phosphorus'))
            potassium = float(request.POST.get('potassium'))
            historical_yield = float(request.POST.get('historical_yield'))
            drainage = request.POST.get('drainage')  # Assuming it's a string or integer that needs no conversion
            crop_variety = request.POST.get('crop_variety')  # Assuming it's a string or integer that needs no conversion
        except ValueError as e:
            # Handle invalid data inputs
            return render(request, 'myapp/predict.html', {'error': 'Invalid input values. Please check your entries.'})
        
        # Prepare the input data for prediction
        input_data = [[soil_ph, water_availability, organic_matter, nitrogen, phosphorus, potassium, historical_yield, drainage, crop_variety]]
        
        # Use the trained model to predict the risk level
        risk_level = model.predict(input_data)

        # Save the prediction in the database
        Prediction.objects.create(
            user=request.user,
            soil_ph=soil_ph,
            water_availability=water_availability,
            organic_matter=organic_matter,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            historical_yield=historical_yield,
            drainage=drainage,
            crop_variety=crop_variety,
            risk_level=risk_level[0],  # Assuming model returns a single value
            recommendation="Recommendation based on model output"  # This can be updated later
        )

        # Render the result page with the prediction
        return render(request, 'myapp/result.html', {'risk_level': risk_level[0]})

    # If the method is not POST, show the prediction form
    return render(request, 'myapp/predict.html')