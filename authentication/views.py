from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from django.shortcuts import redirect, render

from doctor.models import is_doctor

def login_view(request):

    if request.method == "GET":
        if request.user.is_authenticated:
            messages.add_message(
                request, constants.ERROR, "Há um usúario logado. ação bloqueada."
            )
            return redirect("/patient/home")
        return render(request, "login.html")

    elif request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("senha")

        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            if is_doctor(request.user):
                return redirect('/doctors/queries_doctor')                              
            return redirect("/patient/home")

        messages.add_message(
            request,
            constants.ERROR,
            "Credenciais inválidas, entre com credenciais validas",
        )
        return redirect("/authentication/login")


def logout(request):
    auth.logout(request)
    return redirect("/authentication/login")
