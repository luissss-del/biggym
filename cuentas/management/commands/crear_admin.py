from django.core.management.base import BaseCommand
from cuentas.models import Usuario


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Usuario.objects.filter(documento='admin').exists():
            Usuario.objects.create_superuser(
                documento='admin',
                nombre_completo='Administrador',
                sexo='M',
                password='Angelchpo*1103'
            )
            self.stdout.write('Superusuario creado')
        else:
            self.stdout.write('Superusuario ya existe')