from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Medicine)
admin.site.register(Test)
admin.site.register(Contact)
admin.site.register(Schedule)
admin.site.register(Doctor)
admin.site.register(Register)


admin.site.site_header = 'Prescription Management System'
