from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('configurar-dias/', views.configurar_dias_view, name='configurar_dias'),
    path('agregar-dia/', views.agregar_dia_view, name='agregar_dia'),
    path('dia/<int:dia_id>/', views.detalle_dia_view, name='detalle_dia'),
    path('ejercicio/<int:ejercicio_id>/toggle/', views.toggle_ejercicio_view, name='toggle_ejercicio'),
    path('ejercicio/<int:ejercicio_id>/eliminar/', views.eliminar_ejercicio_view, name='eliminar_ejercicio'),
]