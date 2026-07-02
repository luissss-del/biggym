from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, LoginForm


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = RegistroForm()

    return render(request, 'cuentas/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            documento = form.cleaned_data['documento']
            password = form.cleaned_data['password']
            usuario = authenticate(request, username=documento, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('dashboard')
            else:
                messages.error(request, 'Documento o contraseña incorrectos')
    else:
        form = LoginForm()

    return render(request, 'cuentas/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'cuentas/dashboard.html')
