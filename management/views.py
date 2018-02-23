from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django_tables2 import RequestConfig
from .models import (
    Patient,
    HospitalRoom,
    Doctor,
    Appointment,
    Illness,
    Staff,
    RoomAssignment,
    StaffShift
)
from .forms import (
    PatientForm,
    AppointmentForm,
    DoctorForm,
    IllnessForm,
    StaffForm,
    HospitalRoomForm,
    AssignAttendingDoctorForm,
    ScheduleShiftForm
)
from .filters import (
    AppointmentFilter,
    DepartmentRoomFilter,
    StaffFilter,
    ShiftFilterSchedule,
)
from .tables import (
    DoctorTable,
    AppointmentTable,
    PatientAppointmentTable,
    PatientTable,
    IllnessTable,
    StaffTable,
    HospitalRoomTable,
    HospitalRoomsTable,
    StaffScheduleTable

)


def project_overview(request, template_name="project_overview.html"):
    return render(request, template_name, {
        'title': 'Hospital DB Project'
    })


def doctor_list(request, template_name="doctor_list.html"):
    table = DoctorTable(Doctor.objects.all())
    RequestConfig(request).configure(table)
    return render(request, template_name, {
        'title': "Doctor List", 'table': table
    })


# doctor schedule list
def doctor_detail(request, pk, template_name="doctor_detail.html"):
    doctor = get_object_or_404(Doctor, pk=pk)
    appointments = doctor.appointment_set.all()
    appointment_filter = AppointmentFilter(request.GET, queryset=appointments)
    appointment_table = AppointmentTable(appointment_filter.qs)
    num_appointments = appointment_filter.qs.count()
    RequestConfig(request).configure(appointment_table)
    return render(request, template_name, {
        'title': "Doctor Schedule",
        'doctor': doctor,
        'appointment_table': appointment_table,
        'filter': appointment_filter,
        'num_appointments': num_appointments,
    })


def doctor_create(request, template='patient_form.html'):
    form = DoctorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('doctor_list')
    return render(request, template, {
        'form': form,
        'title': 'Create Doctor Record'
    })


def patient_create(request, template_name='patient_form.html'):
    '''Submit submits a post request to this method
    initial page access is a get request to this page

    '''
    form = PatientForm(request.POST or None)

    if form.is_valid():
        # validate results

        form.save()
        return redirect('/management/patient')
    return render(request, template_name, {
        'title': "New Patient Form",
        'form': form
    })


def staff_create(request, template_name='patient_form.html'):
    '''Submit submits a post request to this method
        initial page access is a get request to this page

    '''
    form = StaffForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/management/staff')
    return render(request, template_name, {
        'title': "New Staff Form",
        'form': form
    })


def staff_list(request, template_name='staff_list.html'):
    table_filter = StaffFilter(request.GET, queryset=Staff.objects.all())
    table = StaffTable(table_filter.qs)
    RequestConfig(request).configure(table)
    return render(request, template_name, {
        'title': 'Hospital Staff',
        'table': table,
        'filter': table_filter
    })


def staff_details(request, pk, template_name=''):
    return HttpResponse(Staff.objects.filter(pk=pk))


def appointment_create(request, template_name='appointment_form.html'):
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        appointment = form.save()
        return redirect('doctor', pk=appointment.doctor.pk)
    return render(request, template_name, {
            'title': "Schedule New Appointment",
            'form': form
        })


def patient_detail(request, pk, template_name='patient_detail.html'):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointment_set.all()
    illnesses = patient.illness_set.all()
    illness_table = IllnessTable(illnesses)
    appointment_filter = AppointmentFilter(request.GET, queryset=appointments)
    appointment_table = PatientAppointmentTable(appointment_filter.qs)
    num_appointments = appointment_filter.qs.count()
    RequestConfig(request).configure(appointment_table)
    RequestConfig(request).configure(illness_table)
    return render(request, template_name, {
        'title': 'Patient Records',
        'patient': patient,
        'table': illness_table,
        'appointment_filter': appointment_filter,
        'appointment_table': appointment_table,
        'num_appointments': num_appointments
    })


def patient_list(request, template_name='patient_list.html'):
    table = PatientTable(Patient.objects.all())
    RequestConfig(request).configure(table)
    return render(request, template_name, {
        'title': "Patient List", "table": table
    })


def patient_illness_create(request, template_name='patient_form.html'):
    form = IllnessForm(request.POST or None)
    if form.is_valid():
        pk = form.cleaned_data['patient'].pk
        form = form.save()
        return redirect('/management/patient/{}'.format(pk))

    return render(request, template_name, {
        'title': 'New Patient Record',
        'form': form
    })


def patient_illness_update(request, pk):
    appointment = get_object_or_404(Illness, pk=pk)
    appointment.resolution = 2
    appointment.save()

    return redirect(request.META['HTTP_REFERER'])


def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.soft_delete = True
    appointment.save()

    return redirect(request.META['HTTP_REFERER'])


def staff_member_remove(request, pk):
    staff_member = get_object_or_404(Staff, pk=pk)
    staff_member.soft_delete = True
    staff_member.save()

    return redirect(request.META['HTTP_REFERER'])


def schedule_room(request, template_name='patient_form.html'):
    form = HospitalRoomForm(request.POST or None)

    if form.is_valid():
        patient = form.cleaned_data['patient']
        form.save()
        return redirect('patient', pk=patient.pk)

    return render(request, template_name, {
        'title': 'Room Assignments',
        'form': form
    })


def hospital_rooms(request, template_name='hospital_rooms.html'):
    rooms = HospitalRoom.objects.all()
    room_filter = DepartmentRoomFilter(request.GET, queryset=rooms)
    room_table = HospitalRoomsTable(room_filter.qs)
    num_rooms = room_filter.qs.count()
    RequestConfig(request).configure(room_table)
    return render(request, template_name, {
        'title': 'Hospital Rooms',
        'room_table': room_table,
        'filter': room_filter,
        'num_rooms': num_rooms
    })


def room_assignments(request, template='room_assignment_list.html'):
    table = HospitalRoomTable(RoomAssignment.objects.all())
    RequestConfig(request).configure(table)

    return render(request, template, {
        'title': 'Room Assignments',
        'table': table
    })


def assign_room(request, template='patient_form.html'):

    form = HospitalRoomForm(request.POST or None)

    if form.is_valid():
        room = form.cleaned_data['room']
        room.is_vacant = False
        room.save()
        form.save()
        return redirect('room_assignments')

    return render(request, template, {
        'title': 'Assign Patient Room',
        'form': form
    })


def mark_room_vacant(request, pk):
    room = get_object_or_404(RoomAssignment, pk=pk)
    room.room.is_vacant = True
    room.room.save()
    room.delete()

    return redirect('room_assignments')


def update_patient_room(request, template_name='update_room_info.html'):

    form = AssignAttendingDoctorForm(request.POST or None)

    if form.is_valid():
        patient = form.cleaned_data['patient']
        pk = RoomAssignment.objects.get(patient=patient).pk
        model_inst = get_object_or_404(RoomAssignment, pk=pk)
        for key, value in form.cleaned_data.items():
            setattr(model_inst, key, value)
        model_inst.save()
        return redirect('room_assignments')

    return render(request, template_name, {
        'title': 'Update Patient Room',
        'form': form
    })


def schedule_shift(request, template_name='schedule_shift_form.html'):

    form = ScheduleShiftForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('staff_schedule')
    return render(request, template_name, {
        'title': 'Schedule Staff Member Shift',
        'form': form
    })


def staff_schedule(request, template_name='staff_schedule.html'):

    filter = ShiftFilterSchedule(
        request.GET, queryset=StaffShift.objects.all()
    )
    table = StaffScheduleTable(filter.qs)
    RequestConfig(request).configure(table)
    return render(request, template_name, {
        'title': 'Staff Schedule',
        'filter': filter,
        'table': table
    })


def staff_delete_shift(request, pk):
    shift = get_object_or_404(StaffShift, pk=pk)
    shift.delete()
    return redirect(request.META['HTTP_REFERER'])


def view_operating_room_schedule(request, template_name='staff_schedule.html'):
    filter = AppointmentFilter(request.GET, Appointment.objects.filter(is_surgery=True))
    table = AppointmentTable(filter.qs)
    RequestConfig(request).configure(table)
    return render(request, template_name, {
        'title': 'Scheduled Surgeries',
        'filter': filter,
        'table': table
    })
