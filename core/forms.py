from django import forms
from .models import *

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name','email','age','weight','phone','date','gender','address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile No.'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date':forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'cols':'30', 'rows':'3', 'placeholder': 'Address....', 'id': 'address'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['disease']
        widgets = {
            'disease': forms.Textarea(attrs={'class': 'form-control', 'cols':'50', 'rows':'5', 'placeholder': 'Write Here...'}),
        }

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine']
        widgets = {
            'medicine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Medicine','id':'medicineid','autocomplete':'off'}),
        }

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['test_suggetion']
        widgets = {
            'test_suggetion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Test Suggetion', 'id':'test_suggestid'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','phone','desc']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Phone'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write Here....','cols':'40','rows':'3'}),
        }
