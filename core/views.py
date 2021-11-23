from typing import ContextManager
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse, request
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required,permission_required
from datetime import date
from .filters import *
from .decorators import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
# Create your views here.

def merged_decorator_with_args(lu, per):
    deco1 = permission_required(per)
    deco2 = login_required(login_url=lu)
    def real_decorator(func):
        return deco2(deco1(func))
    return real_decorator

def index_view(request):
    return render(request, 'core/index.html')

def signin_view_doctor(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request,user)
                return redirect('dashboard')
        else:
            form = AuthenticationForm()
    return render (request,'core/signin.html',{'form':form})


@login_required(login_url='signin_doctor')
def signout_view_doctor(request):
    logout(request)
    return redirect('signin_doctor')

# @merged_decorator_with_args('signin', 'core.view_appointment')
@login_required(login_url='signin_doctor')
@user_is_doctor
def dashboard_view(request):
    appoints = Appointment.objects.filter(date = date.today())
    prescribed = Prescription.objects.filter(pres_date = date.today())
    context = {
        'appoints':appoints,
        'app_count':appoints.count(),
        'remaining':max(appoints.count()-prescribed.count(), 0),
        'pres_count':prescribed.count(),
    }
    return render(request, 'core/dashboard.html',context)







def attribute_check(model,pk):
    if hasattr(model, 'prescription'):
        prescript = Prescription.objects.get(appointment_id = pk)
        return prescript
    else:
        prescript = Prescription.objects.create(appointment=model)
        return prescript


@login_required(login_url='signin_doctor')
def prescription_view(request,pk):
    patient = Appointment.objects.get(id=pk)

    if hasattr(patient, 'prescription'):
        prescript = Prescription.objects.get(appointment_id = pk)
        medicines = prescript.medicine_set.all()
        test_suggetions = prescript.test_set.all()
        presform = PrescriptionForm(instance=prescript)
    else:
        presform = PrescriptionForm()
        medicines = {}
        test_suggetions = {}

    if request.method == "POST":
        if hasattr(patient, 'prescription'):
            presform = PrescriptionForm(request.POST,instance=prescript)
        else:
            presform = PrescriptionForm(request.POST)

        form = AppointmentForm(request.POST,instance=patient)
        medicinedata = request.POST['medicine']
        testsuggdata = request.POST['test_suggetion']
        
        medform = MedicineForm({'medicine':medicinedata})
        testform = TestForm({'test_suggetion':testsuggdata})
        
        if presform.is_valid() and medform.is_valid() and form.is_valid():
            form.save()
            new_presform = presform.save(commit=False)
            new_presform.appointment = patient
            new_presform.save()

            if medicinedata.strip() != "":
                new_med = medform.save(commit=False)
                new_med.prescription = new_presform
                new_med.save()
                
            if testsuggdata.strip() != "":
                new_med = testform.save(commit=False)
                new_med.prescription = new_presform
                new_med.save()
        
            if '_prescribe' in request.POST:
                return redirect('dashboard')
            return redirect('prescription',pk)
    
    medform = MedicineForm()
    testform = TestForm()
    form = AppointmentForm(instance=patient)
    context = {
        'form':form,
        'presform':presform,
        'medicine':medform,
        'testform':testform,
        'medicines':medicines,
        'test_suggetions':test_suggetions,
        'patientid':patient.id,
    }
    return render(request, 'core/prescription.html',context)


@login_required(login_url='signin_doctor')
def save_medicine(request):
    patientid = request.POST['patientid']
    patient = Appointment.objects.get(id=patientid)
    prescript = attribute_check(patient,patientid)

    if request.method == 'POST':
        medform = MedicineForm(request.POST)
        if medform.is_valid():
            new_med = medform.save(commit=False)
            new_med.prescription = prescript
            new_med.save()
            medicine_set = prescript.medicine_set.all()
            medicines = list(medicine_set.values())
            return JsonResponse({'status':'Save','medicines':medicines})
        else:
            return JsonResponse({'status':0})


@login_required(login_url='signin_doctor')
def save_test_suggetion(request):
    patientid = request.POST['patientid']
    patient = Appointment.objects.get(id=patientid)
    prescript = attribute_check(patient,patientid)

    if request.method == 'POST':
        testform = TestForm(request.POST)
        if testform.is_valid():
            new_test = testform.save(commit=False)
            new_test.prescription = prescript
            new_test.save()
            test_suggetion_set = prescript.test_set.all()
            test_suggetions = list(test_suggetion_set.values())
            return JsonResponse({'status':'Save','test_suggetions':test_suggetions})
        else:
            return JsonResponse({'status':0})


@login_required(login_url='signin_doctor')
def medicine_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        medicine = Medicine.objects.get(id = id)
        medicine.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})


@login_required(login_url='signin_doctor')
def test_suggetion_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        test = Test.objects.get(id = id)
        test.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})


@login_required(login_url='signin_doctor')
def appointment_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        appoint = Appointment.objects.get(id = id)
        appoint.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

def custom_page_not_found_view(request):
    return render(request, "core/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "core/403.html", {})

@login_required(login_url='signin_doctor')
def presdown_view(request, pk):
    appoint_set = get_object_or_404(Appointment,id = pk)
    if hasattr(appoint_set,'prescription'):
        presdown_set = appoint_set.prescription
        context = {
            'appoint_set': appoint_set,
            'presdown_set': presdown_set
        }
        return render(request, 'pdfdownload.html', context)
    else:
        return custom_page_not_found_view(request)


### all user view ###
def appointment_view(request):
    form = AppointmentForm()
    limit = Schedule.objects.first().limit
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            diff = date.today() - new_form.date
            app_count = Appointment.objects.filter(date = new_form.date).count()

            if diff.days>0:
                messages.error(request, "Please Don't Select Previous Date!!")

            elif app_count>=limit:
                messages.warning(request, "Maximum appointment reached for today. Please choose another date.")

            else:
                serial = app_count+1
                new_form.serial = serial
                new_form.save()
                messages.success(request, serial)
            return redirect('appointment')
            
    context = {
        'form': form,
        }
    return render(request, 'core/appointment.html', context)


def about_view(request):
    return render(request,'core/about.html')


def schedule_view(request):
    schedule_set = Schedule.objects.first()
    context ={
        'schedule_set': schedule_set
    }
    return render(request, 'core/schedule.html', context)


def contact_view(request):
	form = ContactForm()
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your message has been sent!')
			return redirect('contact')
	context = {'form': form}
	return render(request, 'core/contact.html', context)



@login_required(login_url='signin_doctor')
def all_patient_view(request):
    appoints = Appointment.objects.order_by('-date')
    context = {
        'appoints':appoints,
    }
    return render(request, 'core/all_patient_view.html',context)


@login_required(login_url='signin_doctor')
def all_patient_filter(request):
    if request.method == 'GET':
        appoints = []
        appoint_set = {}

        if 'uid' in request.GET:
            uid = request.GET.get('uid')
            appoint_set = Appointment.objects.filter(id = uid)

        if 'name' in request.GET:
            name = request.GET.get('name')
            appoint_set = Appointment.objects.filter(name__icontains = name)

        if 'date' in request.GET:
            date = request.GET.get('date')
            appoint_set = Appointment.objects.filter(date__icontains = date)
            
        appoints = list(appoint_set.values())
        if appoints:
            return JsonResponse({'status':1,'appoints':appoints})
        else:
            return JsonResponse({'status':0})
    else:
        return JsonResponse({'status':0})






@login_required(login_url='signin_doctor')
def med_test_update(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        Value = request.GET.get('value')
        type = request.GET.get('type')
        if type == 'medicine':
            medicine = Medicine.objects.get(id = id)
            medicine.medicine = Value
            medicine.save()
        elif type == 'test_sugg':
            test = Test.objects.get(id = id)
            test.test_suggetion = Value
            test.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})


def auto_med(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        medicine_set = Medicine.objects.filter(medicine__icontains = query)
        medicines = []
        for med in medicine_set:
            medicines.append(med.medicine)
        return JsonResponse({'status':1,'medicines':medicines})
    else:
        return JsonResponse({'status':0})





def change_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context =  {
        'form':form
    }
    return render (request,'core/userchange.html',context)

def paying_status(request):
    status = request.GET.get('status')
    id = request.GET.get('id')

    appointment = Appointment.objects.get(id = id)
    # print('before:',appointment.paying_status)
    appointment.paying_status = status
    # print('after:',appointment.paying_status)
    appointment.save()

    context = {}
    return JsonResponse(context)


def check_status_view(request):
    check_status = request.GET.get('check')
    id = request.GET.get('id')

    appointment = Appointment.objects.get(id = id)
    # print('before:',appointment.check_status)
    appointment.check_status = check_status
    # print('after:',appointment.check_status)
    appointment.save()

    context = {}
    return JsonResponse(context)


def signin_view_register(request):
    if request.user.is_authenticated:
        return redirect('register')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request,user)
                return redirect('register')
        else:
            form = AuthenticationForm()
    return render (request,'core/signin.html',{'form':form})


@login_required(login_url='signin_register')
def signout_view_register(request):
    logout(request)
    return redirect('signin_register')




@login_required(login_url='signin_register')
@user_is_register
def register_dashboard(request):
    appoints = Appointment.objects.filter(date = date.today())
    prescribed = Prescription.objects.filter(pres_date = date.today())

    form = AppointmentForm()
    limit = Schedule.objects.first().limit
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        # print(request.POST)
        
        name = request.POST.get("name")
        age =  request.POST.get("age")
        phone =  request.POST.get("phone")
        gender =  request.POST.get("gender")
        cdate = request.POST.get("date")

        app_count = Appointment.objects.filter(date = cdate).count()
        if app_count>=limit:
            messages.warning(request, "Maximum appointment reached for today. Please choose another date.")

        else:
            serial = app_count+1
            Appointment.objects.create(name = name , age = age , phone = phone , gender = gender, serial = serial)

            messages.success(request, serial)
        return redirect('register')

    context = {
        'form': form,
        'appoints':appoints,
        'app_count':appoints.count(),
        'remaining':max(appoints.count()-prescribed.count(), 0),
        'pres_count':prescribed.count(),
    }
    return render(request, 'core/register_dashboard.html', context)


def appointment_update(request, pk):
    appoint = Appointment.objects.get(id=pk)

    form = AppointmentForm(instance=appoint)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance= appoint)
        if form.is_valid():
            form.save()
            messages.success(request, "Your information successfully saved!")
            return redirect('updates', pk)
    context = {
        'form':form
    }
    return render(request, 'core/update.html', context)
