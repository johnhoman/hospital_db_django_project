import django_filters
from .models import (
    Appointment,
    HospitalRoom,
    Staff,
    StaffShift
)


class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = ['date']


class DepartmentRoomFilter(django_filters.FilterSet):
    class Meta:
        model = HospitalRoom
        fields = [
            'department'
        ]


class StaffFilter(django_filters.FilterSet):

    class Meta:
        model = Staff
        fields = [
            'occupation',
        ]


class ShiftFilterSchedule(django_filters.FilterSet):

    class Meta:
        model = StaffShift
        fields = [
            'date',
        ]
