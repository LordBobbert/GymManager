from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('client', 'Client'),
    )
    
    # Role Field
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    
    # Common Fields for All Users
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    birthdate = models.DateField()
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)

    # By default, 'username' is required and will be used for logging in
    REQUIRED_FIELDS = ['email']  # Email is a required field, but login is with 'username'

    def __str__(self):
        return f"{self.username} - {self.role}"

# Trainer Profile
class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'trainer'})
    employment_status = models.CharField(
        max_length=20,
        choices=[('subcontractor', 'Subcontractor'), ('employee', 'Employee')],
    )
    rent_rate_monthly = models.DecimalField(max_digits=6, decimal_places=2)
    rent_rate_per_session = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Trainer: {self.user.username}"

# Client Profile
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'client'})
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    training_rate = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive'), ('vacation', 'Vacation')],
        default='active',
    )
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Client: {self.user.username}"
