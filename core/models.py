from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.
class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    class Meta:
        permissions = [
            ("can_view_register", "can_view_register"),
        ]

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    class Meta:
        permissions = [
            ("can_view_doctor", "can_view_doctor"),
        ]




class Appointment(models.Model):
    person = (
        ('','Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )

    status = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )

    check_choices = (
        ('Visited', 'Visited'),
        ('Unvisited', 'Unvisited'),
    )

    name = models.CharField(max_length=122, null=True)
    email = models.CharField(max_length=122, null=True)
    age = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    phone = models.CharField(max_length=122, null=True)
    gender = models.CharField(max_length=122, choices = person,null=True)
    paying_status = models.CharField(max_length=122, choices = status,null=True, default= 'Unpaid')
    check_status = models.CharField(max_length=122, choices = check_choices,null=True, default='Unvisited')
    address = models.TextField(max_length=255, null=True)
    date = models.DateField(default=date.today,null=True)
    serial = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    class Meta:
        permissions = (("can_view_all", "can_view_all"),)


class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment,on_delete=models.SET_NULL,null=True)
    disease = models.CharField(max_length=122, null=True,blank=True)
    pres_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return "Serial #{}".format(self.id)

class Medicine(models.Model):
    prescription = models.ForeignKey(Prescription,on_delete=models.SET_NULL,null=True)
    medicine = models.CharField(max_length=122, null=True,blank=True)
    def __str__(self):
        return f"{self.medicine}"

class Test(models.Model):
    prescription = models.ForeignKey(Prescription,on_delete=models.SET_NULL,null=True)
    test_suggetion = models.CharField(max_length=122, null=True,blank=True)
    def __str__(self):
        return f"{self.test_suggetion}"



class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    Saturday = models.CharField(max_length=122, blank= True, null=True)
    Sunday = models.CharField(max_length=122, blank= True, null=True)
    Monday = models.CharField(max_length=122, blank= True, null=True)
    Tuesday = models.CharField(max_length=122, blank= True, null=True)
    Wednesday = models.CharField(max_length=122, blank= True, null=True)
    Thursday = models.CharField(max_length=122, blank= True, null=True)
    Friday = models.CharField(max_length=122, blank= True, null=True)
    limit = models.IntegerField(default=0, null=True)

    def __str__(self):
        return "Weekly Schedule"
