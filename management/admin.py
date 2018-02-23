from django.contrib import admin
from .models import (
    Patient, 
    Appointment,
    Doctor,
    Illness,
    Staff,
    Department,
    HospitalRoom,
    Occupation,
    RoomAssignment,
    Nurse
)

# Register your models here.
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Illness)
admin.site.register(Staff)
admin.site.register(Department)
admin.site.register(HospitalRoom)
admin.site.register(Occupation)
admin.site.register(RoomAssignment)
admin.site.register(Nurse)
