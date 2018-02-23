from django import forms
from .models import (
    Patient,
    Doctor,
    Appointment,
    Illness,
    Staff,
    RoomAssignment,
    StaffShift
)

from pprint import pprint


class PatientNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} {} {}".format(obj.first_name, obj.last_name, obj.last_four())


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = (
            'first_name',
            'last_name',
            'social_security_number',
            'date_of_birth',
            'sex',
            'age',
            'street_address',
            'city',
            'state',
            'phone_number',
        )


class AppointmentForm(forms.ModelForm):
    patient = PatientNameChoiceField(queryset=Patient.objects.all())

    class Meta:
        model = Appointment
        fields = (
            'doctor',
            'patient',
            'date',
            'start_time',
            'end_time',
            'is_surgery',
        )


class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = (
            'first_name',
            'last_name',
            'social_security_number',
            'specialization',
        )

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)


class StaffForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = (
            'first_name',
            'last_name',
            'social_security_number',
            'occupation',
            'specialization'
        )


class IllnessForm(forms.ModelForm):

    class Meta:
        model = Illness
        fields = (
            'doctor',
            'patient',
            'illness',
            'prescribed_medication',
            'date_diagnosed',
            'resolution'
        )

    def __init__(self, *args, **kwargs):
        super(IllnessForm, self).__init__(*args, **kwargs)


class IllnessUpdateForm(forms.ModelForm):

    class Meta:
        model = Illness
        fields = (
            'resolution',
        )


class HospitalRoomForm(forms.ModelForm):

    class Meta:
        model = RoomAssignment
        fields = (
            'room',
            'patient',
        )


class AssignAttendingDoctorForm(forms.ModelForm):

    class Meta:
        model = RoomAssignment
        fields = (
            'patient',
            'doctor',
            'nurse'
        )


class AssignAttendingNurseForm(forms.ModelForm):

    class Meta:
        model = RoomAssignment
        fields = (
            'patient',
            'nurse',
        )


class ScheduleShiftForm(forms.ModelForm):

    class Meta:
        model = StaffShift

        fields = (
            'staff_member',
            'date',
            'start_time',
            'end_time',
        )




