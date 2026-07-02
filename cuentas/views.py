from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import RegistroForm, LoginForm, ConfigurarDiasForm, EjercicioForm
from .models import DiaEntrenamiento, Ejercicio


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
    dias = DiaEntrenamiento.objects.filter(usuario=request.user)

    if not dias.exists():
        return redirect('configurar_dias')

    dias_ordenados = sorted(dias, key=lambda d: d.orden_dia())

    return render(request, 'cuentas/dashboard.html', {
        'dias': dias_ordenados,
        'dias_choices': DiaEntrenamiento.DIAS_CHOICES,
    })


@login_required
def configurar_dias_view(request):
    if request.method == 'POST':
        dias_seleccionados = request.POST.getlist('dias')
        if dias_seleccionados:
            for dia in dias_seleccionados:
                parte_cuerpo = request.POST.get(f'parte_cuerpo_{dia}', '').strip()
                if parte_cuerpo:
                    DiaEntrenamiento.objects.update_or_create(
                        usuario=request.user,
                        dia=dia,
                        defaults={'parte_cuerpo': parte_cuerpo}
                    )
            return redirect('dashboard')
        else:
            messages.error(request, 'Selecciona al menos un día')

    return render(request, 'cuentas/configurar_dias.html', {
        'dias': DiaEntrenamiento.DIAS_CHOICES
    })





@login_required
def detalle_dia_view(request, dia_id):
    dia_entrenamiento = get_object_or_404(DiaEntrenamiento, id=dia_id, usuario=request.user)
    ejercicios = dia_entrenamiento.ejercicios.all()

    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            ejercicio = form.save(commit=False)
            ejercicio.dia_entrenamiento = dia_entrenamiento
            ejercicio.save()
            return redirect('detalle_dia', dia_id=dia_entrenamiento.id)
    else:
        form = EjercicioForm()

    return render(request, 'cuentas/detalle_dia.html', {
        'dia_entrenamiento': dia_entrenamiento,
        'ejercicios': ejercicios,
        'form': form,
    })


@login_required
@require_POST
def toggle_ejercicio_view(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id, dia_entrenamiento__usuario=request.user)
    ejercicio.completado = not ejercicio.completado
    ejercicio.save()
    return JsonResponse({'completado': ejercicio.completado})


@login_required
@require_POST
def eliminar_ejercicio_view(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id, dia_entrenamiento__usuario=request.user)
    dia_id = ejercicio.dia_entrenamiento.id
    ejercicio.delete()
    return redirect('detalle_dia', dia_id=dia_id)


@login_required
@require_POST
def agregar_dia_view(request):
    dias_seleccionados = request.POST.getlist('dias')
    for dia in dias_seleccionados:
        parte_cuerpo = request.POST.get(f'parte_cuerpo_{dia}', '').strip()
        if parte_cuerpo:
            DiaEntrenamiento.objects.update_or_create(
                usuario=request.user,
                dia=dia,
                defaults={'parte_cuerpo': parte_cuerpo}
            )
    return redirect('dashboard')