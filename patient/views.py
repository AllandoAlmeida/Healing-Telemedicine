from datetime import datetime
from django.shortcuts import render, redirect
from doctor.models import MedicalData, OpenDate, Specialties, is_doctor
from django.contrib.messages import constants
from django.contrib import messages

from django import template
from django.utils.formats import date_format

from patient.models import Query, Document
from django.contrib.auth.decorators import login_required

@login_required
# Create your views here.
def home(request):
    if request.method == "GET":
        doctors = MedicalData.objects.all()
        specialties = Specialties.objects.all()
        doctor_filter = request.GET.get('medico')
        filter_by_specialties = request.GET.getlist('especialidades')
 
        
        if doctor_filter:
            doctors = doctors.filter(name__icontains=doctor_filter)
        
        if filter_by_specialties:
            doctors = doctors.filter(specialty_id__in=filter_by_specialties)
            
      
        if not doctors.exists():  
            messages.add_message(request, constants.WARNING, 'Lamentamos! não foi possível localizar o médico pesquisado.')

        return render(request, 'home.html', {'doctors': doctors, 'specialties': specialties, 'is_doctor': is_doctor(request.user)})


@login_required   
def select_times(request, id_medical_data):
   
    
    if request.method == "GET":
        doctor = MedicalData.objects.get(id=id_medical_data)
        available_dates = OpenDate.objects.filter(user=doctor.user).filter(date__gt=datetime.now()).filter(scheduled=False).order_by('date')
        return render(request, 'select_times.html', {'doctor': doctor, 'available_dates': available_dates, 'is_doctor': is_doctor(request.user)})
 



@login_required   
def schedule_time(request, open_date_id):
    if request.method == "GET":
        open_date = OpenDate.objects.get(id=open_date_id)

        scheduled_time = Query(
            patient=request.user,
            open_date=open_date
        )

        scheduled_time.save()

        # TODO: Sugestão Tornar atomico

        open_date.scheduled = True
        open_date.save()

        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')

        return redirect('/patient/my_queries/')


@login_required 
def my_queries(request):
    # realizar os filtros
    if request.method == "GET":
        filterDate = request.GET.get('data')
        filterSpecialties = request.GET.get('especialidades')
        specialties = Specialties.objects.all()
        print("specialties", specialties)
        queries_scheduled = Query.objects.filter(patient=request.user).filter(open_date__date__gte=datetime.now())
        print("queries_scheduled", )
        
        
        if filterDate:
            queries_scheduled = queries_scheduled.filter(open_date__date__gte=filterDate)
            
        
        if filterSpecialties:
            queries_scheduled = queries_scheduled.filter(open_date__user__medicaldata__specialty__id=filterSpecialties)
            
        return render(request, 'my_queries.html', {
            'queries_scheduled': queries_scheduled,
            'specialties' : specialties,
            'filterDate': filterDate,
            'filterSpecialties':filterSpecialties,
            'is_doctor': is_doctor(request.user)
        })
        

@login_required      
def query(request, id_query):
    if request.method == 'GET':
        query = Query.objects.get(id=id_query)
        medical_data = MedicalData.objects.get(user=query.open_date.user)
        documents = Document.objects.filter(query=query)
        return render(request, 'query.html', {'query': query, 'medical_data': medical_data, 'documents': documents,  'is_doctor': is_doctor(request.user)})

         
def cancel_scheduled_appointment(request, id_query):
    query = Query.objects.get(id=id_query)
    if request.user != query.patient:
        messages.add_message(request, constants.ERROR, 'Solicitação não autorizada, somente quem realizou o agendamento podera cancelar!')
        return redirect(f'/authentication/logout')
    
    query.status = 'C'
    query.save()
    
    return redirect('/patient/my_queries/')
    