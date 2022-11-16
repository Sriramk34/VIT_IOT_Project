from django.contrib import admin

# Register your models here.
from .models import device
from .models import userDetails
from .models import sensor

admin.site.register(device)
admin.site.register(userDetails)
admin.site.register(sensor)

