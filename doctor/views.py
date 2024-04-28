from patient.models import  Query, Document
from .models import Specialties, MedicalData, is_doctor, OpenDate

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants

from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count



# Create your views here.

@login_required
def register_doctor(request):

    if is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Você ja está cadastro como médico')
        return redirect('/doctors/schedule_time')

    if request.method == "GET":
        specialties = Specialties.objects.all()
        for i in specialties:            
            print(i.id, i.specialty)        
        return render(request, 'register_doctor.html', {'specialties':specialties, 'is_doctor': is_doctor(request.user)})
    elif request.method == "POST":
        name = request.POST.get('nome')
        zidCode = request.POST.get('cep')
        street = request.POST.get('rua')
        neighborhood = request.POST.get('bairro')
        number = request.POST.get('numero')
        description = request.POST.get('descricao')
        query_value = request.POST.get('valor_consulta')
        crm = request.POST.get('crm')
        medical_identity_card = request.FILES.get('cim')
        register_geral = request.FILES.get('rg')
        photo = request.FILES.get('foto')
        specialty_id = request.POST.get('especialidade')  # Obtendo o ID da especialidade

        medical_data = MedicalData(
            user=request.user,
            name=name,
            zidCode=zidCode,
            street=street,
            neighborhood=neighborhood,
            number=number,
            description=description,
            query_value=query_value,
            crm=crm,
            medical_identity_card=medical_identity_card,
            register_geral=register_geral,
            photo=photo,
            specialty_id=specialty_id  # Atribuindo o ID da especialidade
        )
        print(medical_data)
        medical_data.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso')
        return redirect('/doctors/open_calendar')
    
    
@login_required   
def open_calendar(request):
    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/authentication/logout')
    
    if request.method == "GET":
        medical_data = MedicalData.objects.get(user=request.user)
        open_appointments = OpenDate.objects.filter(user=request.user)
        return render(request, 'open_calendar.html', {'medical_data': medical_data, 'open_appointments':open_appointments, 'is_doctor': is_doctor(request.user)})
    
    if request.method == "POST":
        date = request.POST.get('date')
        
        date_format = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        
        if date_format <= datetime.now():
            messages.add_message(request, constants.WARNING, 'A data não pode ser anterior a data atual')
            return redirect('/doctors/open_calendar')
        
        scheduled_date = OpenDate(
            date=date,
            user=request.user,
        )
        
        scheduled_date.save()
        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso')
        
        return redirect('/doctors/open_calendar')        
    
@login_required 
def queries_doctor(request):
    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/authentication/logout')
    
    doctor = MedicalData.objects.get(user=request.user)  # Obtém um único objeto MedicalData
    print('doctor specialty:', doctor.specialty)
    
    today = datetime.now().date()
    queries_today = Query.objects.filter(open_date__user=request.user).filter(open_date__date__gte=today).filter(open_date__date__lt=today + timedelta(days=1))
    remaining_queries = Query.objects.exclude(id__in=queries_today.values('id')).filter(open_date__user=request.user)
    
    return render(request, 'queries_doctor.html', {'queries_today': queries_today, 'remaining_queries': remaining_queries, 'is_doctor': is_doctor(request.user), 'doctor':doctor})


@login_required
def consultation_area_doctor(request, id_query):
    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/authentication/logout')
    

    if request.method == "GET":
        query = Query.objects.get(id=id_query)
        documents = Document.objects.filter(query = query)
        return render(request, 'consultation_area_doctor.html', {'query': query, 'documents':documents, 'is_doctor': is_doctor(request.user)}) 
    
    elif request.method == "POST": 
        query = Query.objects.get(id=id_query)
        link = request.POST.get('link')
        
        if query.status == 'C':
            messages.add_message(request, constants.WARNING, 'Essa consulta ja esta cancelada')
            return redirect(f'/doctors/consultation_area_doctor/{id_query}')
        
        elif query.status == 'F':
            messages.add_message(request, constants.WARNING, 'Essa consulta ja esta cancelada')
            return redirect(f'/doctors/consultation_area_doctor/{id_query}')
        
@login_required
def end_query(request, id_query):
    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/authentication/logout')
    
    query = Query.objects.get(id=id_query)
    if request.user != query.open_date.user:
        messages.add_message(request, constants.ERROR, 'Solicite ao médico responsavel autorização para realizar essa solicitação.')
        return redirect('/authentication/logout')
    
    
    query.status = 'F'
    query.save()
    return redirect(f'/doctors/consultation_area_doctor/{id_query}')

@login_required
def add_document(request, id_query):
    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Solicite ao médico responsavel autorização para realizar essa solicitação.')
        return redirect('/authentication/logout')
    
    query = Query.objects.get(id=id_query)
    if request.user != query.open_date.user:
        messages.add_message(request, constants.ERROR, 'Solicite ao médico responsavel autorização para realizar essa solicitação.')
        return redirect('/authentication/logout')
    
    
    title = request.POST.get('titulo')
    document = request.FILES.get('documento')

    if not document:
        messages.add_message(request, constants.WARNING, 'Adicione o documento.')
        return redirect(f'/doctors/consultation_area_doctor/{id_query}')

    document = Document(
        query=query,
        title=title,
        document=document

    )

    document.save()

    messages.add_message(request, constants.SUCCESS, 'Documento adicionando com sucesso!')
    return redirect(f'/doctors/consultation_area_doctor/{id_query}')


@login_required
def dashboard(request):
    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Solicite ao médico responsavel autorização para realizar essa solicitação.')
        return redirect('/authentication/logout')
    
    queries = Query.objects.filter(open_date__user=request.user).filter(open_date__date__range=[datetime.now().date() - timedelta(days=7), datetime.now().date() + timedelta(days=1)]).annotate().annotate(amount=Count('id'))
    
    dates = [i['open_date__date'].strftime("%d-%m-%Y") for i in queries]
    amount = [i['amount'] for i in queries]
    
    return render(request, 'dashboard.html', {'dates': dates, 'amount': amount})

    