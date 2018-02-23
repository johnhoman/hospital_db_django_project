import django_tables2 as tables
from django_tables2.utils import A
from .models import (
    Doctor,
    Appointment,
    Patient,
    Illness,
    Staff,
    RoomAssignment,
    HospitalRoom,
    StaffShift
)


class DoctorTable(tables.Table):
    view = tables.LinkColumn(
        'doctor',
        orderable=False, text='View Schedule', args=[A('pk')]
    )

    class Meta:
        model = Doctor
        template = 'django_tables2/bootstrap.html'
        attr = {'class': 'table'}
        fields = (
                'view',
                'first_name',
                'last_name',
                'specialization',
                )


class StaffTable(tables.Table):

    view = tables.LinkColumn(
        'staff_details',
        orderable=False,
        text='View Staff Info',
        args=[A('pk')]
    )
    remove = tables.LinkColumn(
        'staff_member_remove',
        orderable=False,
        text='Remove Staff Member',
        args=[A('pk')]
    )

    class Meta:
        model = Staff
        template = 'django_tables2/bootstrap.html'
        attr = {'class': 'table'}
        fields = (
            'view',
            'first_name',
            'last_name',
            'occupation',
            'social_security_number',
            'remove'
        )


class AppointmentTable(tables.Table):
    action = tables.LinkColumn(
        'appointment_delete',
        orderable=False,
        text='cancel',
        args=[A('pk')]
    )

    class Meta:
        model = Appointment
        template = 'django_tables2/bootstrap.html'
        attr = {'class': 'table table-striped'}
        fields = (
            'date',
            'start_time',
            'end_time',
            'patient',
            'doctor',
            'action',
        )


class PatientAppointmentTable(tables.Table):

    action = tables.LinkColumn('appointment_delete', orderable=False, text='cancel', args=[A('pk')])

    class Meta:
        model = Appointment
        template = 'django_tables2/bootstrap.html'
        attr = {'class': 'table table-striped'}
        fields = (
            'date',
            'start_time',
            'end_time',
            'doctor',
            'action'
        )


class PatientTable(tables.Table):
    view = tables.LinkColumn('patient', orderable=False, text='View Patient Info', args=[A('pk')])

    class Meta:
        model = Patient
        template = 'django_tables2/bootstrap.html'
        attr = {'class': 'table'}
        fields = (
            'view',
            'first_name',
            'last_name',
            'social_security_number'
        )


class IllnessTable(tables.Table):

    update = tables.LinkColumn('patient_illness_update', orderable=False, text='Mark Resolved', args=[A('pk')])

    class Meta:
        model = Illness
        template = 'django_tables2/bootstrap.html'
        attr = {'class': 'table'}
        fields = (
            'doctor',
            'illness',
            'prescribed_medication',
            'date_diagnosed',
            'resolution',
            'update'
        )


class HospitalRoomTable(tables.Table):

    action = tables.LinkColumn('mark_room_vacant', text='Mark Vacant', orderable=False, args=[A('pk')])

    class Meta:
        model = RoomAssignment
        template = 'django_tables2/bootstrap.html'
        attr = {'class': 'table'}
        fields = (
            'patient',
            'room',
            'doctor',
            'nurse'
        )


class HospitalRoomsTable(tables.Table):

    class Meta:
        model = HospitalRoom
        template = 'django_tables2/bootstrap.html'
        attr = {'class': 'table'}
        fields = (
            'room_number',
            'department',
            'is_vacant'
        )


class StaffScheduleTable(tables.Table):
    action = tables.LinkColumn(
            'staff_delete_shift', text='cancel shift', orderable=False, args=[A('pk')]
        )
    class Meta:
        model = StaffShift
        template = 'django_tables2/bootstrap.html'
        attr = {'class': 'table'}
        fields = (
            'staff_member',
            'staff_member.occupation',
            'staff_member.specialization',
            'date',
            'start_time',
            'end_time'
        )





