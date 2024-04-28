from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages

from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.method == "GET":        
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem.')
            return redirect('/users/register')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve ter pelo menos 6 caracteres.')
            return redirect('/users/register')
        
        users = User.objects.filter(username=username)
        
        if users.exists():
            messages.add_message(request, constants.ERROR, 'Username já utilizado, escolha outro.')
            return redirect('/users/register')
        
        try:  # Tente criar o usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=senha
            )
            messages.add_message(request, constants.SUCCESS, "Usuário cadastrado com sucesso")
        
            return redirect('/authentication/login')
        except IntegrityError:
            messages.add_message(request, constants.ERROR, 'O nome de usuário ou email já existe.')
            return redirect('/users/register')
        except Exception as e:  # Lidar com outros erros
            messages.add_message(request, constants.ERROR, 'Erro ao criar usuário: {}'.format(e))
            return redirect('/users/register')
        
        


""" 
# Médicos homens

medico2 = Medico(54321, "Dr. Marcos Oliveira", "54321-876", "Avenida Brasil", "Jardim Botânico", 50, "Especialista em Ortopedia", 250.00, "marcosortho", "marcosortho@example.com", "Medico@01", "Medico@01")
medico3 = Medico(98765, "Dr. Ricardo Santos", "98765-432", "Rua do Sol", "Praia do Mar", 20, "Clínico Geral", 150.00, "ricardoclinic", "ricardoclinic@example.com", "Medico@01", "password789")
medico4 = Medico(24680, "Dr. André Costa", "24680-135", "Travessa da Paz", "Centro", 80, "Especialista em Pediatria", 180.00, "andreped", "andreped@example.com", "Medico@01", "passwordabc")
medico5 = Medico(13579, "Dr. Eduardo Almeida", "13579-642", "Rua dos Médicos", "Hospitalar", 10, "Especialista em Neurologia", 300.00, "eduardoneuro", "eduardoneuro@example.com", "Medico@01", "Medico@01")
medico1 = Medico(12345, "Dr. João Silva", "12345-678", "Rua das Flores", "Centro", 100, "Especialista em Cardiologia", 200.00, "dr_joao", "dr.joaosilva@example.com", "Medico@01", "Medico@01")

# Médicas mulheres

medica1 = Medico(11111, "Dra. Ana Oliveira", "11111-222", "Avenida das Rosas", "Jardim Primavera", 30, "Ginecologista", 220.00, "ana_gyn", "ana_gyn@example.com", "Medico@01", "Medico@01")
medica2 = Medico(22222, "Dra. Camila Santos", "22222-333", "Rua das Oliveiras", "Centro", 15, "Dermatologista", 180.00, "camiladerm", "camiladerm@example.com", "Medico@01", "Medico@01")
medica3 = Medico(33333, "Dra. Fernanda Costa", "33333-444", "Avenida dos Lírios", "Praia Azul", 25, "Psiquiatra", 260.00, "fernanda_psych", "fernanda_psych@example.com", "Medico@01", "Medico@01")
medica4 = Medico(44444, "Dra. Marina Lima", "44444-555", "Rua das Margaridas", "Vale Verde", 40, "Oftalmologista", 240.00, "marina_eyes", "marina_eyes@example.com", "Medico@01", "Medico@01")
medica5 = Medico(55555, "Dra. Juliana Pereira", "55555-666", "Avenida dos Passarinhos", "Bosque Feliz", 35, "Nutricionista", 200.00, "juliana_nutri", "juliana_nutri@example.com", "Medico@01", "Medico@01")


paciente1 = Paciente("paciente01", "paciente01@example.com", "password123", "password123")
paciente2 = Paciente("paciente02", "paciente02@example.com", "password456", "password456")
paciente3 = Paciente("paciente03", "paciente03@example.com", "password789", "password789")
paciente4 = Paciente("paciente04", "paciente04@example.com", "passwordabc", "passwordabc")
paciente5 = Paciente("paciente05", "paciente05@example.com", "passwordxyz", "passwordxyz")

"""