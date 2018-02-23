import datetime

from django.db import models

'''
on_delete=models.CASCADE in foreign key,
removes entry if foreign key entry is deleted
'''


RESOLUTION = (
    (1, "treatment in progress"),
    (2, "Cured"),
)


class Occupation(models.Model):
    name = models.CharField(max_length=255, default='N/A')

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255, default='N/A')

    def __str__(self):
        return self.name


class Patient(models.Model):

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    social_security_number = models.CharField(
            max_length=11,
            default='xxx-xx-xxxx',
            unique=True
        )
    date_of_birth = models.DateField(default=datetime.datetime.now())
    phone_number = models.CharField(max_length=14, default='(xxx) xxx-xxxx')
    street_address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=255, default='')

    def last_four(self):
        return self.social_security_number.split('-')[-1]

    def __str__(self):
        return "%s, %s (xxx-xx-%s)" % (
                self.last_name,
                self.first_name,
                self.last_four()
            )


class HospitalRoom(models.Model):
    room_number = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    is_vacant = models.BooleanField(default=True)

    def __str__(self):
        return "Room %d: %s" % (
            self.room_number, self.department
        )


class StaffManagement(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(soft_delete=False)


class Staff(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    social_security_number = models.CharField(max_length=256, unique=True)
    occupation = models.ForeignKey(Occupation, on_delete=models.PROTECT)
    specialization = models.ForeignKey(Department, on_delete=models.PROTECT)
    soft_delete = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=14, default='(xxx) xxx-xxxx')
    street_address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    salary = models.FloatField(default=0)

    def __str__(self):
        return "%s %s: %s" % (
            self.first_name, self.last_name, self.occupation
        )

    objects = StaffManagement()


class DoctorManager(models.Manager):

    def get_queryset(self):
        return super(DoctorManager, self).get_queryset()\
            .filter(occupation__name='Doctor').filter(soft_delete=False)


class Doctor(Staff):

    class Meta:
        proxy = True

    def __str__(self):
        return "Dr. {} {}: {}".format(
            self.first_name, self.last_name, self.specialization
        )

    objects = DoctorManager()


class NurseManager(models.Manager):

    def get_queryset(self):
        return super(NurseManager, self).get_queryset()\
                .filter(occupation__name='Nurse').filter(soft_delete=False)


class Nurse(Staff):

    class Meta:
        proxy = True

    def __str__(self):
        return "{} {}, RN".format(
            self.first_name, self.last_name
        )

    objects = NurseManager()


class AppointmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(soft_delete=False)


class Appointment(models.Model):
    class Meta:
        ordering = ['date', 'start_time']

    date = models.DateField(default=datetime.datetime.now())
    start_time = models.CharField(default='', max_length=128)
    end_time = models.CharField(default='', max_length=128)
    soft_delete = models.BooleanField(default=False)
    description = models.CharField(max_length=1024, default='N/A')
    is_surgery = models.BooleanField(default=False)

    patient = models.ForeignKey(
            Patient,
            on_delete=models.PROTECT,
            blank=True,
            null=True
        )
    doctor = models.ForeignKey(
            Doctor,
            on_delete=models.PROTECT
        )

    objects = AppointmentManager()

    def __str__(self):
        return "{}: {} - {}".format(
                self.date.strftime('%A, %B %d, %Y'),
                self.start_time,
                self.end_time
            )


class Illness(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    illness = models.CharField(max_length=255, default='')
    prescribed_medication = models.CharField(max_length=255, default='')
    date_diagnosed = models.DateField(default=datetime.datetime.now())
    resolution = models.IntegerField(choices=RESOLUTION, default=1)

    def __str__(self):
        return "{}: {}".format(self.patient, self.illness)


class RoomAssignment(models.Model):
    room = models.ForeignKey(
            HospitalRoom,
            on_delete=models.PROTECT,
            unique=True
        )
    patient = models.ForeignKey(
            Patient,
            on_delete=models.PROTECT
        )
    doctor = models.ForeignKey(
            Doctor,
            on_delete=models.PROTECT,
            blank=True,
            null=True,
            related_name='attending_doctor'
        )

    nurse = models.ForeignKey(
        Nurse, on_delete=models.PROTECT, blank=True,
        null=True, related_name='attending_nurse'
    )


class StaffShift(models.Model):

    staff_member = models.ForeignKey(Staff, on_delete=models.PROTECT)
    date = models.DateField(default=datetime.datetime.now())
    start_time = models.CharField(default='9:00 AM', max_length=8)
    end_time = models.CharField(default='5:00 PM', max_length=8)

    def __str__(self):
        return "{}:{}:{} - {}".format(
            self.staff_member, self.date, self.start_time, self.end_time
        )
