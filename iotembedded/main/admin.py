from django.contrib import admin

# Register your models here.
from .models import device
from .models import userDetails

admin.site.register(device)
admin.site.register(userDetails)


