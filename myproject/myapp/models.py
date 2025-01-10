from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .managers import CustomUserManager
from django.core.validators import FileExtensionValidator
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model


class Role(models.Model):
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, fullname, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        return self.email

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the prediction to a user
    
    # Additional feature fields from the dataset
    soil_ph = models.FloatField()  # Soil pH
    water_availability = models.FloatField()  # Water Availability in mm
    organic_matter = models.FloatField()  # Organic Matter (%) 
    nitrogen = models.FloatField()  # Nitrogen (%) 
    phosphorus = models.FloatField()  # Phosphorus (ppm)
    potassium = models.FloatField()  # Potassium (ppm)
    historical_yield = models.FloatField()  # Historical Yield (kg/ha)
    
    # Categorical features
    drainage = models.CharField(max_length=50)  # Drainage condition (e.g., Excellent, Poor)
    crop_variety = models.CharField(max_length=100)  # Crop Variety (e.g., Variety C, Variety F)
    
    # Prediction result fields
    risk_level = models.CharField(max_length=100)  # Risk Level (e.g., Medium, High)
    recommendation = models.TextField()  # Recommendation for the user
    
    # Date when the prediction is made
    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.user.username} on {self.prediction_date}"

    class Meta:
        # Optional: Add ordering and other model meta options
        ordering = ['-prediction_date']  # Order predictions by most recent first    