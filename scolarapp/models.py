from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.management.utils import get_random_secret_key
import random
import string


# Create your models here.
class Role (models.Model):
    
    ROLE_CHOICES = [
        ("Administrateur", "Administrateur"),
        ("Étudiant", "Étudiant"),
        ("Enseignant", "Enseignant"),
        ("Parent","Parent"),
        ("Chauffeur", "Chauffeur"),  # Ajout du rôle de chauffeur
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,choices=ROLE_CHOICES,default='Étudiant')

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='schools_logo/', blank=True, null=True)
    address = models.CharField(max_length=255,null = True, blank = True)
    phone_number = models.CharField(max_length=255,null = True, blank = True)
    semestre = models.CharField(max_length=255, null = True , blank = True)
    # Ajoutez d'autres champs nécessaires pour votre modèle d'école

    def __str__(self):
        return self.name

class EducationLevel(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, related_name='education_levels', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.school.name})"

class Classroom(models.Model):

    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    school=models.ForeignKey(School, related_name='classrooms',on_delete=models.CASCADE)
    occupied = models.BooleanField(null=True,blank=True)

    def __str__(self):
        return f"{self.name} ({self.school.name})"
    
class Subject(models.Model):

    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,blank=True,null=True)
    education_level = models.ForeignKey(EducationLevel,on_delete=models.CASCADE,null=True,blank=True)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    coefficient = models.DecimalField(max_digits=4, decimal_places=2, null = True, blank = True)  # Coefficient du contrôle

    def __str__(self):
        return self.name
    
class User(AbstractUser):

    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        default='profile_pictures/profile_picture.png',  # Chemin relatif dans le bucket S3
        blank=True, 
        null=True
    ) 
    role=models.ForeignKey(Role, on_delete=models.CASCADE,null=True)
    gender = models.CharField(max_length=10, choices=[("MALE", "Male"), ("FEMALE", "Female")], blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)  # Clé étrangère vers le modèle School
    is_verified = models.BooleanField(default=False)
    email =models.EmailField(unique=True)
    
    # Champs spécifiques aux étudiants
    classroom = models.CharField(max_length=100, blank=True, null=True)
    absences_number = models.IntegerField(default=0, null=True, blank=True)
    payment_done = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    transportation_service = models.BooleanField(default=False)
    parent_key = models.CharField(max_length=255, null=True , blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)

    # Champs spécifiques aux enseignants
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    paid = models.BooleanField(default=False)
    education_level=models.ForeignKey(EducationLevel,max_length=100,on_delete=models.CASCADE,null=True,blank=True)
    # education_level = models.ManyToManyField(EducationLevel, blank=True)  # Relation Many-to-Many

    monthly_salary = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # Champ de salaire
    session_salary = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # Champ de salaire

    parent = models.ForeignKey(  # Relation Parent-Étudiant
        'self',  # Relation vers le même modèle
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',  # Facilite l'accès aux enfants depuis le parent
        limit_choices_to={'role__name': 'Parent'}  # Limite les choix aux utilisateurs ayant le rôle "Parent"
    )

    def generate_parent_key(self):
        self.parent_key = ''.join(random.choices(string.ascii_letters + string.digits, k=10))


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    
class Timetable(models.Model):
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emploi du temps - {self.education_level.name} ({self.school.name})"
        
class TimetableSession(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetable, related_name="sessions", on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__name': 'Enseignant'})
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE,null=True,blank=True)
    education_level=models.ForeignKey(EducationLevel,on_delete=models.CASCADE)
    day = models.CharField(max_length=50, choices=[
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.subject.name} - {self.teacher} ({self.classroom.name})"
    

class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Sujet/matière du cours
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__name': 'Enseignant'})  # Professeur associé
    school = models.ForeignKey(School, on_delete=models.CASCADE)  # École associée au cours
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE)  # Niveau d'éducation

    def __str__(self):
        return f"{self.subject.name} - {self.teacher.first_name} {self.teacher.last_name} ({self.school.name})"


class CourseFile(models.Model):
    course = models.ForeignKey(Course, related_name='files', on_delete=models.CASCADE)  # Clé étrangère vers le cours
    file = models.FileField(upload_to='course_files/')  # Fichier téléversé
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Date de téléversement
    file_type = models.CharField(max_length=100, blank=True, null=True)  # Type de fichier libre


    def __str__(self):
        return f"Fichier pour {self.course.subject.name} - {self.course.teacher.first_name} {self.course.teacher.last_name}"


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

class TransportLocation(models.Model):

    transport = models.ForeignKey('Transport', on_delete=models.CASCADE, related_name='transport_locations')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()  # Indique l'ordre des arrêts si nécessaire

    class Meta:
        ordering = ['order']  # Les locations seront ordonnées par cet ordre pour chaque transport

    def __str__(self):
        return f"{self.transport} - {self.location} (Stop {self.order})"


class Transport(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    registration = models.CharField(max_length=20, blank=True, null=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__name': 'Chauffeur'}, related_name='driven_transports')
    students = models.ManyToManyField(User, limit_choices_to={'role__name': 'Étudiant'}, related_name='student_transports')  # Plusieurs étudiants par transport
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='transports')  # Clé étrangère vers School

    def __str__(self):
        return self.registration

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="events")

    def __str__(self):
        return f"{self.title} - {self.date}"
    
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('earning', 'Earning'),
    ]

    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)  # Choix entre 'expense' et 'earning'
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Montant de la transaction
    date = models.DateField(default=timezone.now)  # Date de la transaction
    description = models.TextField(blank=True, null=True)  # Description facultative
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='transactions')  # Clé étrangère vers l'école


    class Meta:
        ordering = ['-date']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} on {self.date}"
    
class TeacherAvailability(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role__name': 'Enseignant'},
        related_name='availabilities'
    )
    day = models.CharField(
        max_length=50,
        choices=[
            ('Lundi', 'Lundi'),
            ('Mardi', 'Mardi'),
            ('Mercredi', 'Mercredi'),
            ('Jeudi', 'Jeudi'),
            ('Vendredi', 'Vendredi'),
            ('Samedi', 'Samedi'),
            ('Dimanche', 'Dimanche'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='teacher_availabilities'
    )

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name} - {self.day} ({self.start_time} à {self.end_time})"


class Control(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role__name': 'Enseignant'},
        related_name='controls'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='controls'
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='controls'
    )
    education_level = models.ForeignKey(
        EducationLevel,
        on_delete=models.CASCADE,
        related_name='controls'
    )

    control_number = models.PositiveIntegerField()  # Numéro ou ordre du contrôle
    control_type = models.CharField(max_length=100)  # Type de contrôle libre (DS, Quiz, DL, etc.)
    coefficient = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)  # Coefficient du contrôle
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return f"{self.subject.name} - {self.control_type} {self.control_number} (Coeff: {self.coefficient})"

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__name': 'Étudiant'}, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True,null=True)  # Note de l'étudiant
    comments = models.TextField(blank=True, null=True)  # Commentaires facultatifs de l'enseignant
    education_level=models.ForeignKey(EducationLevel,max_length=100,on_delete=models.CASCADE,null=True,blank=True)
    control = models.ForeignKey(Control, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.subject.name} : {self.score}"

class ChatRoom(models.Model):
    """
    Représente une salle de chat simple entre deux utilisateurs.
    """
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_rooms_user1"
    )  # Premier utilisateur
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_rooms_user2"
    )  # Deuxième utilisateur
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return f"ChatRoom entre {self.user1.first_name} et {self.user2.first_name}"


class Message(models.Model):
    """
    Représente un message envoyé entre deux utilisateurs dans une salle de chat.
    """
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )  # Salle de chat associée
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )  # Expéditeur du message
    file = models.FileField(upload_to="chat_files/", null=True, blank=True)  # Fichier joint
    content = models.TextField(null=True,blank=True)  # Contenu du message
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création du message

    def __str__(self):
        return f"Message de {self.sender.first_name} dans {self.chat_room}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Nouveau champ
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, blank=True)  # Référence au chat

    def __str__(self):
        return f"Notification for {self.user.username} - Read: {self.is_read}"
    
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='timeslots')

    def __str__(self):
        return f"{self.start_time} - {self.end_time} ({self.school.name})"

class Notice(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='notices')
    created_at = models.DateTimeField(auto_now_add=True)
    roles = models.ManyToManyField('Role', related_name='notices')

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class HomeworkBook(models.Model):
    """Model representing a homework book entry for a teacher."""
    
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__name': 'Enseignant'})
    education_level = models.ForeignKey(
        "EducationLevel",  # Replace with your corresponding model
        on_delete=models.CASCADE,
        related_name="homework_books",
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    homework_due_date = models.DateField(verbose_name="Homework Due Date")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Homework Book"
        verbose_name_plural = "Homework Books"

    def __str__(self):
        return f"{self.title} - {self.education_level} - {self.teacher}"
