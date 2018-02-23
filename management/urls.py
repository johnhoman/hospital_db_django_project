from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', project_overview, name='index'),
    url(r'^patient/$', patient_list, name='patient_list'),
    url(r'^patient/(?P<pk>\d+)/$', patient_detail, name='patient'),
    url(r'^patient/create/$', patient_create, name='patient_create'),
    url(r'^appointment/create/$', appointment_create, name='appointment_create'),
    url(r'^appointment/delete/(?P<pk>\d+)/$', appointment_delete, name='appointment_delete'), 
    url(r'^doctor/$', doctor_list, name='doctor_list'),
    url(r'^doctor/(?P<pk>\d+)/$', doctor_detail, name='doctor'),
    url(r'^doctor/create/$', doctor_create, name='doctor_create'),
    url(r'^patient/illness/create/$', patient_illness_create, name='patient_illness_create'),
    url(r'^staff/$', staff_list, name='staff'),
    url(r'^staff/(?P<pk>\d+)/$', staff_details, name='staff_details'),
    url(r'^staff/create/$', staff_create, name='staff_create'),
    url(r'^schedule/room/$', schedule_room, name='schedule_room'),
    url(r'^patient/illness/update/(?P<pk>\d+)/$', patient_illness_update, name='patient_illness_update'),
    url(r'^staff/member/remove/(?P<pk>\d+)/$', staff_member_remove, name='staff_member_remove'),
    url(r'^room/assignments/$', room_assignments, name='room_assignments'),
    url(r'^room/assignments/assign/$', assign_room, name='assign_room'),
    url(r'^room/assignments/free/(?P<pk>\d+)/$', mark_room_vacant, name='mark_room_vacant'),
    url(r'^hospital/rooms/$', hospital_rooms, name='hospital_rooms'),
    url(r'^update/room/info/$', update_patient_room, name='update_room_info'),
    url(r'^staff/schedule/shift/$', schedule_shift, name='staff_schedule_shift'),
    url(r'^staff/schedule/$', staff_schedule, name='staff_schedule'),
    url(r'^staff/schedule/shift/delete/(?P<pk>\d+)?/$', staff_delete_shift, name='staff_delete_shift'),
    url(r'^patient/scheduled/surgeries/$', view_operating_room_schedule, name='view_operation_room_schedule')
]
