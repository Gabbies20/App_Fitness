# Generated by Django 4.2.8 on 2023-12-14 09:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ejercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('tipo_ejercicio', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Entrenamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('duracion', models.IntegerField()),
                ('tipo', models.CharField(choices=[('AER', 'Aeróbico'), ('FUE', 'Fuerza o anaeróbico'), ('FUN', 'Funcional'), ('HIT', 'Hit'), ('POT', 'Potencia')], default='HIT', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='EntrenamientoPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrenamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.entrenamiento')),
            ],
        ),
        migrations.CreateModel(
            name='PlanEntrenamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('duracion_estimada', models.IntegerField()),
                ('dificultad', models.CharField(max_length=20)),
                ('fecha_inicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_fin', models.DateTimeField(default=django.utils.timezone.now)),
                ('entrenamientos', models.ManyToManyField(through='fitness.EntrenamientoPlan', to='fitness.entrenamiento')),
            ],
        ),
        migrations.CreateModel(
            name='RutinaDiaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('descripcion', models.TextField()),
                ('duracion', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contraseña', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('comentario', models.TextField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.ejercicio')),
                ('u_creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco', models.CharField(choices=[('CAI', 'Caixa'), ('BBV', 'BBVA'), ('UNI', 'Unicaja'), ('ING', 'ING España')], default='ING', max_length=3)),
                ('numero_cuenta', models.CharField(max_length=20)),
                ('titular', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fitness.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='SeguimientoPlanEntrenamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_fin', models.DateTimeField(default=django.utils.timezone.now)),
                ('progreso', models.IntegerField()),
                ('plan_entrenamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.planentrenamiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='RutinaEjercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.ejercicio')),
                ('rutina_diaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.rutinadiaria')),
            ],
        ),
        migrations.AddField(
            model_name='rutinadiaria',
            name='ejercicios',
            field=models.ManyToManyField(through='fitness.RutinaEjercicio', to='fitness.ejercicio'),
        ),
        migrations.AddField(
            model_name='rutinadiaria',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.usuario'),
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('descuento', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='planentrenamiento',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.usuario'),
        ),
        migrations.CreateModel(
            name='Perfil_de_Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edad', models.IntegerField()),
                ('altura', models.FloatField()),
                ('peso', models.FloatField()),
                ('foto_perfil', models.ImageField(upload_to='imagenes/')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fitness.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialEjercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('duracion', models.IntegerField(default=0)),
                ('repeticiones', models.IntegerField(default=0)),
                ('peso', models.FloatField(default=0)),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.ejercicio')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='entrenamientoplan',
            name='plan_entrenamiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.planentrenamiento'),
        ),
        migrations.CreateModel(
            name='EntrenamientoEjercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repeticiones', models.IntegerField(default=0)),
                ('peso_utilizado', models.FloatField(default=0)),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.ejercicio')),
                ('entrenamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.entrenamiento')),
            ],
        ),
        migrations.AddField(
            model_name='entrenamiento',
            name='ejercicios',
            field=models.ManyToManyField(through='fitness.EntrenamientoEjercicio', to='fitness.ejercicio'),
        ),
        migrations.AddField(
            model_name='entrenamiento',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.usuario'),
        ),
        migrations.AddField(
            model_name='ejercicio',
            name='usuarios',
            field=models.ManyToManyField(through='fitness.HistorialEjercicio', to='fitness.usuario'),
        ),
        migrations.AddField(
            model_name='ejercicio',
            name='usuarios_votos',
            field=models.ManyToManyField(related_name='usuarios_votos', through='fitness.Voto', to='fitness.usuario'),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('entrenamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.entrenamiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaEjercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('grupo_muscular_principal', models.CharField(max_length=50)),
                ('ejercicios', models.ManyToManyField(to='fitness.ejercicio')),
            ],
        ),
    ]
