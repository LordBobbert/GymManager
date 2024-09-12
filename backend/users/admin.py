from django.contrib import admin
from .models import User, TrainerProfile, ClientProfile

admin.site.register(User)
admin.site.register(TrainerProfile)
admin.site.register(ClientProfile)
