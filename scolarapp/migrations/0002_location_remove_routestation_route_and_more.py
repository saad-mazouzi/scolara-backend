# Generated by Django 5.1.2 on 2025-01-08 16:08

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='routestation',
            name='route',
        ),
        migrations.RemoveField(
            model_name='routestation',
            name='station',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='number',
        ),
        migrations.AddField(
            model_name='school',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='schools_logo/'),
        ),
        migrations.AddField(
            model_name='school',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='semestre',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='coefficient',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='education_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scolarapp.educationlevel'),
        ),
        migrations.AddField(
            model_name='timetablesession',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='scolarapp.school'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transport',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='transport',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transports', to='scolarapp.school'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transport',
            name='students',
            field=models.ManyToManyField(limit_choices_to={'role__name': 'Étudiant'}, related_name='student_transports', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='monthly_payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='monthly_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='next_payment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='parent_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='session_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='transportation_service',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transport',
            name='driver',
            field=models.ForeignKey(limit_choices_to={'role__name': 'Chauffeur'}, on_delete=django.db.models.deletion.CASCADE, related_name='driven_transports', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='absences_number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_rooms_user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_rooms_user2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('control_number', models.PositiveIntegerField()),
                ('control_type', models.CharField(max_length=100)),
                ('coefficient', models.DecimalField(decimal_places=2, default=1.0, max_digits=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('education_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to='scolarapp.educationlevel')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to='scolarapp.school')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to='scolarapp.subject')),
                ('teacher', models.ForeignKey(limit_choices_to={'role__name': 'Enseignant'}, on_delete=django.db.models.deletion.CASCADE, related_name='controls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scolarapp.educationlevel')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scolarapp.school')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scolarapp.subject')),
                ('teacher', models.ForeignKey(limit_choices_to={'role__name': 'Enseignant'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='course_files/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('file_type', models.CharField(blank=True, max_length=100, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='scolarapp.course')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='scolarapp.school')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('control', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scolarapp.control')),
                ('education_level', models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='scolarapp.educationlevel')),
                ('student', models.ForeignKey(limit_choices_to={'role__name': 'Étudiant'}, on_delete=django.db.models.deletion.CASCADE, related_name='grades', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='scolarapp.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='chat_files/')),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chat_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='scolarapp.chatroom')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('chat_room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scolarapp.chatroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi'), ('Dimanche', 'Dimanche')], max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_availabilities', to='scolarapp.school')),
                ('teacher', models.ForeignKey(limit_choices_to={'role__name': 'Enseignant'}, on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeslots', to='scolarapp.school')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('expense', 'Expense'), ('earning', 'Earning')], max_length=7)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='scolarapp.school')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='TransportLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scolarapp.location')),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transport_locations', to='scolarapp.transport')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.DeleteModel(
            name='Route',
        ),
        migrations.DeleteModel(
            name='RouteStation',
        ),
        migrations.DeleteModel(
            name='TransportStation',
        ),
    ]
