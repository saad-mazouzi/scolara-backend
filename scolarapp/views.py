from django.shortcuts import render
from .models import Role,User,EducationLevel,School,Classroom,Timetable,Subject,TimetableSession,CourseFile,Course,Grade,Transaction,TeacherAvailability,Control,ChatRoom,Message,Notice
from .serializers import UserSerializer,RoleSerializer,EducationLevelSerializer,SchoolSerializer,ClassroomSerializer,TimetableSerializer,SubjectSerializer,TimetableSessionSerializer,CourseFileSerializer,CourseSerializer,GradeSerializer,TransactionSerializer,TeacherAvailabilitySerializer,ControlSerializer,ChatRoomSerializer,MessageSerializer, NotificationSerializer,NoticeSerializer
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from sib_api_v3_sdk.rest import ApiException
from rest_framework.decorators import action
from .models import Transport,Location,TransportLocation, Notification
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import AccessToken, TokenError,RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from rest_framework import viewsets,status,filters
from django.views.decorators.http import require_GET
from .permissions import IsAdmin,IsAdminOrReadOnly,IsOwner
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from .sendinblue_service import send_verification_email,send_reset_password_email,send_sms
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
import random,string
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
import requests
from django.db.models import Q
from django.conf import settings
from .serializers import TransportSerializer,LocationSerializer,TransportLocationSerializer
from .models import Event
from .serializers import EventSerializer
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Max, Min
from django.db.models import Sum, F
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models.signals import post_save
from rest_framework.response import Response
from .serializers import TimeSlotSerializer
from .models import TimeSlot
from datetime import date,datetime,timedelta
from django.db.models import Q, Count




# Create your views here.
class RoleViewset(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class ControlViewSet(viewsets.ModelViewSet):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer


    def get_queryset(self):

        queryset = self.queryset
        school_id = self.request.query_params.get('school_id')
        education_level = self.request.query_params.get('education_level')
        subject = self.request.query_params.get('subject')
        teacher = self.request.query_params.get('teacher')

        if school_id:
            queryset = queryset.filter(school_id=school_id)

        if education_level:
            queryset = queryset.filter(education_level=education_level)

        if subject:
            queryset = queryset.filter(subject=subject)

        if teacher:
            queryset = queryset.filter(teacher=teacher)

        return queryset
    
class TeacherAvailabilityViewset(viewsets.ModelViewSet):
    queryset = TeacherAvailability.objects.all()
    serializer_class = TeacherAvailabilitySerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @action(detail=True, methods=['put'], url_path='update_logo')
    def update_logo(self, request, pk=None):
        school = self.get_object()
        logo = request.FILES.get('logo', None)

        if not logo:
            return Response({'error': 'Aucun logo fourni.'}, status=status.HTTP_400_BAD_REQUEST)

        school.logo = logo
        school.save()

        return Response({'message': 'Logo mis à jour avec succès.', 'logo': school.logo.url}, status=status.HTTP_200_OK)

class CourseViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        education_level_id = self.request.query_params.get('education_level')
        
        queryset = Course.objects.all()

        if school_id:
            queryset = queryset.filter(school_id=school_id)
        
        if education_level_id:
            queryset = queryset.filter(education_level_id=education_level_id)
        
        return queryset

    
class CourseFileViewset(viewsets.ModelViewSet):
    queryset = CourseFile.objects.all()
    serializer_class = CourseFileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        subject_id = self.request.query_params.get('subject')
        
        if subject_id:
            queryset = queryset.filter(course__subject_id=subject_id)
        
        return queryset


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class TransportLocationViewSet(viewsets.ModelViewSet):
    queryset = TransportLocation.objects.all()
    serializer_class = TransportLocationSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        if school_id is not None:
            return Transport.objects.filter(school_id=school_id)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        transport_data = request.data
        stations_data = transport_data.pop('stations', [])

        serializer = self.get_serializer(data=transport_data)
        serializer.is_valid(raise_exception=True)
        transport = serializer.save()

        for station_data in stations_data:
            location, created = Location.objects.get_or_create(
                latitude=station_data['latitude'],
                longitude=station_data['longitude'],
                defaults={'address': station_data.get('address', '')}
            )
            TransportLocation.objects.create(
                transport=transport,
                location=location,
                order=station_data['order']
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        transport = self.get_object()

        # Récupérer les locations liées au transport et les supprimer
        locations_to_delete = [tl.location for tl in transport.transport_locations.all()]

        # Supprimer d'abord les relations dans TransportLocation
        transport.transport_locations.all().delete()

        # Supprimer ensuite les locations
        for location in locations_to_delete:
            location.delete()

        # Supprimer le transport
        transport.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 

class ClassroomViewset(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        if school_id:
            return Classroom.objects.filter(school_id=school_id)
        return Classroom.objects.all()
    
class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        education_level_id = self.request.query_params.get('education_level_id')
        
        queryset = self.queryset
        if school_id:
            queryset = queryset.filter(school_id=school_id)
        if education_level_id:
            queryset = queryset.filter(education_level_id=education_level_id)
        return queryset

class TimetableSessionViewSet(viewsets.ModelViewSet):
    queryset = TimetableSession.objects.all()
    serializer_class = TimetableSessionSerializer

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        education_level = self.request.query_params.get('education_level')
        
        queryset = TimetableSession.objects.all()
        
        if school_id:
            queryset = queryset.filter(school_id=school_id)
        
        if education_level:
            queryset = queryset.filter(education_level=education_level)
        
        return queryset
    


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer

    def get_queryset(self):
        user = self.request.user  # Récupérer l'utilisateur connecté

        # Vérifier si l'utilisateur est authentifié
        if not user.is_authenticated:
            return Notice.objects.none()  # Aucun avis pour les utilisateurs non connectés

        school_id = self.request.query_params.get('school_id')

        # Si l'utilisateur est un administrateur, il peut voir les avis de son école uniquement
        if user.role and user.role.name == "Administrateur":
            if user.school:
                queryset = Notice.objects.filter(school=user.school)
            else:
                return Notice.objects.none()

            # Si un school_id est fourni, s'assurer qu'il correspond à l'école de l'administrateur
            if school_id and int(school_id) != user.school.id:
                return Notice.objects.none()

            return queryset

        # Si l'utilisateur n'a pas de rôle, il ne voit aucun avis
        if not hasattr(user, 'role') or not user.role:
            return Notice.objects.none()

        queryset = Notice.objects.all()

        # Filtrer par école si `school_id` est fourni
        if school_id:
            queryset = queryset.filter(school_id=school_id)

        # Filtrer par rôle de l'utilisateur connecté
        queryset = queryset.filter(roles__id=user.role.id)

        return queryset
    
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_notice(self, request, pk=None):
        """
        Supprime un avis spécifique si l'utilisateur est Administrateur.
        """
        user = request.user

        if not user.is_authenticated or not user.role or user.role.name != "Administrateur":
            return Response({"error": "Permission refusée"}, status=status.HTTP_403_FORBIDDEN)

        try:
            notice = Notice.objects.get(pk=pk)
            notice.delete()
            return Response({"message": "Avis supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
        except Notice.DoesNotExist:
            return Response({"error": "Avis introuvable"}, status=status.HTTP_404_NOT_FOUND)
    
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        education_level_id = self.request.query_params.get('education_level_id')  # Mettez à jour ici

        print(f"School ID: {school_id}, Education Level ID: {education_level_id}")  # Débogage

        
        queryset = Subject.objects.all()
        
        if school_id:
            queryset = queryset.filter(school_id=school_id)
        
        if education_level_id:
            queryset = queryset.filter(education_level_id=education_level_id)  # Correspond à la requête frontend
        
        return queryset



class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def create(self, request, *args, **kwargs):
        print("Données reçues par l'API :", request.data)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
            education_level_id = self.request.query_params.get('education_level')
            subject_id = self.request.query_params.get('subject_id')
            user_id = self.request.query_params.get('user_id')  # Ajouter le paramètre user_id

            queryset = Grade.objects.all()

            if education_level_id:
                queryset = queryset.filter(education_level_id=education_level_id)

            if subject_id:
                queryset = queryset.filter(subject_id=subject_id)

            if user_id:
                queryset = queryset.filter(student_id=user_id)  # Filtrer par étudiant

            return queryset
    
    @action(detail=False, methods=['get'])
    def subject_statistics(self, request):
        """
        Custom action to calculate the min, max, and average grades for a specific subject_id.
        """
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({"error": "subject_id is required"}, status=400)

        grades = self.get_queryset().filter(subject_id=subject_id)

        if not grades.exists():
            return Response({"error": "No grades found for the specified subject_id"}, status=404)

        stats = grades.aggregate(
            min_grade=Min('score'),
            max_grade=Max('score'),
            avg_grade=Avg('score')
        )

        return Response({
            "subject_id": subject_id,
            "min_grade": round(stats['min_grade'], 2) if stats['min_grade'] is not None else None,
            "max_grade": round(stats['max_grade'], 2) if stats['max_grade'] is not None else None,
            "avg_grade": round(stats['avg_grade'], 2) if stats['avg_grade'] is not None else None
        })
    
    @action(detail=False, methods=['get'])
    def class_average(self, request):
        """
        Custom action to calculate the weighted average for a class (education level).
        """
        education_level_id = self.request.query_params.get('education_level_id')
        if not education_level_id:
            return Response({"error": "education_level_id is required"}, status=400)

        # Récupérer les sujets associés au niveau d'éducation
        subjects = Subject.objects.filter(education_level_id=education_level_id)
        if not subjects.exists():
            return Response({"error": "No subjects found for the specified education level"}, status=404)

        total_weighted_scores = 0
        total_coefficients = 0

        for subject in subjects:
            # Filtrer les notes par matière
            grades = self.get_queryset().filter(subject_id=subject.id)

            if grades.exists():
                # Calculer la moyenne des notes pour cette matière
                subject_avg = grades.aggregate(avg_grade=Avg('score'))['avg_grade']
                if subject_avg is not None:
                    # Ajouter au total pondéré
                    total_weighted_scores += subject_avg * subject.coefficient
                    total_coefficients += subject.coefficient

        if total_coefficients == 0:
            return Response({"error": "The total coefficients sum is zero, cannot calculate average"}, status=400)

        # Calculer la moyenne générale pondérée
        class_average = total_weighted_scores / total_coefficients

        return Response({
            "class_average": round(class_average, 2) if class_average is not None else None
        })

    
class EducationLevelViewset(viewsets.ModelViewSet):
    queryset=EducationLevel.objects.all()
    serializer_class=EducationLevelSerializer
    
    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        if school_id:
            return EducationLevel.objects.filter(school_id=school_id)
        return EducationLevel.objects.all()

    @action(detail=False, methods=['get'], url_path='my-education-levels')
    def my_education_levels(self, request):
        user = request.user
        if user.role and user.role.name == "Enseignant":  # Vérifier que l'utilisateur est un enseignant
            education_levels = user.education_level.all()  # Many-to-Many relation
            serializer = self.get_serializer(education_levels, many=True)
            return Response(serializer.data)
        return Response({"detail": "Not allowed"}, status=403)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    serializer_class = UserSerializer

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        education_level_id = self.request.query_params.get('education_level')
        subject_id = self.request.query_params.get('subject_id')
        role_id = self.request.query_params.get('role_id')  # Nouveau paramètre

        queryset = User.objects.all()

        if role_id:
            queryset = queryset.filter(role_id=role_id)  # Filtrer par rôle

        if school_id:
            queryset = queryset.filter(school_id=school_id)
        
        if education_level_id:
            queryset = queryset.filter(education_level_id=education_level_id)
        
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        return queryset


    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        data = request.data
        is_admin = data.get('is_admin', False)  # Vérifiez si l'utilisateur est un admin

        if is_admin:
            # Si l'utilisateur est un administrateur, utilisez le nom de l'école
            school_name = data.get('school')
            school, created = School.objects.get_or_create(name=school_name)  # Créez ou récupérez l'école
            data['school'] = school.id  # Remplacez le nom par l'ID de l'école

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(data['password'])  # Chiffrer le mot de passe

            user.generate_parent_key()

            user.save()

            # Envoyer l'email de vérification
            send_verification_email(user)

            return Response({
                'message': 'Utilisateur enregistré avec succès. Veuillez vérifier votre email.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=False, methods=['get'])
    def get_role(self, request):
        user = request.user

        # Vérification si l'utilisateur est authentifié
        if user.is_anonymous:
            return Response(
                {"detail": "Utilisateur non authentifié."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        role = user.role.name if user.role else None
        return Response({'role': role}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')  # Récupérer l'e-mail
        password = request.data.get('password')  # Récupérer le mot de passe
        
        try:
            user = User.objects.get(email=email)  # Trouver l'utilisateur par e-mail
            print(f"Utilisateur trouvé : {user.email}, rôle : {user.role.name}")
            if user.check_password(password):  # Vérifier le mot de passe
                refresh = RefreshToken.for_user(user)
                response = JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'first_name': user.first_name,
                    'school': user.school.name if user.school else None,
                    'school_id': user.school.id if user.school else None,
                    'user': UserSerializer(user).data
                })
                return response
            else:
                print(f"Mot de passe incorrect pour l'utilisateur {user.email}")
                return JsonResponse({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            print("Utilisateur introuvable avec cet e-mail :", email)
            return JsonResponse({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'status': 'success', 'message': 'Logged out successfully.'})
    
    @action(detail=False, methods=['get'])
    def get_students(self, request):
        # Récupérer l'ID de l'école depuis les cookies
        school_id = request.GET.get('school_id')
        
        if not school_id:
            return Response(
                {"error": "Aucun ID d'école trouvé dans les cookies."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrer les utilisateurs par rôle étudiant (id=2) et par école
        students = User.objects.filter(role__id=2, school__id=school_id)
        serializer = UserSerializer(students, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_parents(self, request):
        # Récupérer l'ID de l'école depuis les cookies
        school_id = request.GET.get('school_id')
        
        if not school_id:
            return Response(
                {"error": "Aucun ID d'école trouvé dans les cookies."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrer les utilisateurs par rôle étudiant (id=2) et par école
        parents = User.objects.filter(role__id=4, school__id=school_id)
        serializer = UserSerializer(parents, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_students_by_education_level(self, request):
        school_id = request.query_params.get('school_id')
        education_level_id = request.query_params.get('education_level')  # Utilisation de l'ID
        
        if not school_id:
            return Response(
                {"error": "Aucun ID d'école fourni."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrer les étudiants par école
        students = User.objects.filter(role__name='Étudiant', school__id=school_id)
        
        # Appliquer un filtre supplémentaire sur l'ID du niveau d'éducation si spécifié
        if education_level_id:
            students = students.filter(education_level__id=education_level_id)

        
        # Sérialiser les résultats
        serializer = UserSerializer(students, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_drivers(self, request):
        # Récupérer l'ID de l'école depuis les cookies
        school_id = request.GET.get('school_id')
        
        if not school_id:
            return Response(
                {"error": "Aucun ID d'école trouvé dans les cookies."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrer les utilisateurs par rôle chauffeur (id=5) et par école
        drivers = User.objects.filter(role__id=5, school__id=school_id)
        serializer = UserSerializer(drivers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def update_driver(self, request, pk=None):
        # Récupérer le chauffeur en vérifiant son rôle
        driver = get_object_or_404(User, pk=pk, role__name='Chauffeur')
        data = request.data

        # Mettre à jour les champs du chauffeur si fournis
        driver.first_name = data.get('first_name', driver.first_name)
        driver.last_name = data.get('last_name', driver.last_name)
        driver.email = data.get('email', driver.email)
        driver.phone_number = data.get('phone_number', driver.phone_number)
        driver.address = data.get('address', driver.address)
        driver.school_id = data.get('school', driver.school_id)
        driver.paid = data.get('paid', driver.paid)  # Ajout ici
        # Mettre à jour le nombre d'absences et les salaires
        driver.monthly_salary = data.get('monthly_salary', driver.monthly_salary)

        # next_payment_date = data.get('next_payment_date', None)
        # if next_payment_date:
        #     driver.next_payment_date = next_payment_date


        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            driver.profile_picture = profile_picture

        # Récupérer l'instance du sujet (optionnel), si fourni
        subject_id = data.get('subject')
        if subject_id:
            try:
                subject_instance = Subject.objects.get(id=subject_id)
                driver.subject = subject_instance  # Assigner l'instance du sujet
            except Subject.DoesNotExist:
                return Response(
                    {"detail": "Le sujet spécifié n'existe pas."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            driver.subject = None  # Gérer le cas où aucun sujet n'est fourni

        # Gestion de l'image de profil (optionnel)
        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            driver.profile_picture = profile_picture

        # Mettre à jour le mot de passe si fourni
        password = data.get('password', None)
        if password:
            driver.set_password(password)

        driver.save()

        return Response(
            {'message': 'Chauffeur mis à jour avec succès.', 'driver': UserSerializer(driver).data},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['delete'])
    def delete_driver(self, request, pk=None):
        # Récupérer le chauffeur en vérifiant son rôle
        driver = get_object_or_404(User, pk=pk, role__name='Chauffeur')
        
        # Supprimer le chauffeur
        driver.delete()
        
        return Response({"detail": "Chauffeur supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def get_teacher(self, request):
        # Récupérer l'ID de l'école depuis les cookies
        school_id = request.GET.get('school_id')

        
        if not school_id:
            return Response(
                {"error": "Aucun ID d'école trouvé dans les cookies."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrer les enseignants (role__id=3) par école
        teachers = User.objects.filter(role__id=3, school__id=school_id)
        serializer = UserSerializer(teachers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def create_student(self, request):
        data = request.data
        default_role, created = Role.objects.get_or_create(name='Étudiant')

        # Générer un nom d'utilisateur unique
        first_name = data.get('first_name', '').lower()
        last_name = data.get('last_name', '').lower()
        random_number = ''.join(random.choices(string.digits, k=4))
        username = f"{first_name}.{last_name}{random_number}"

        # Vérifier si le nom d'utilisateur est déjà utilisé
        while User.objects.filter(username=username).exists():
            random_number = ''.join(random.choices(string.digits, k=4))
            username = f"{first_name}.{last_name}{random_number}"

        student = User(
            username=username,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone_number=data.get('phone_number', ''),
            address=data.get('address', ''),
            role=default_role,
            school_id=data.get('school'),
            education_level_id=data.get('education_level'),
            gender=data.get('gender')  # Ajoutez le champ gender ici
        )

        # Générer la clé parent avant de sauvegarder
        student.generate_parent_key()

        # Gestion de l'image de profil
        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            student.profile_picture = profile_picture

        # Gestion du mot de passe
        password = data.get('password')
        if password:
            student.set_password(password)
        else:
            student.set_unusable_password()

        student.save()

        return Response(
            {'message': 'Étudiant créé avec succès.', 'student': UserSerializer(student).data},
            status=status.HTTP_201_CREATED
        )
    

    @action(detail=False, methods=['post'])
    def create_parent(self, request):
        data = request.data
        default_role, created = Role.objects.get_or_create(name='Parent')

        # Générer un nom d'utilisateur unique
        first_name = data.get('first_name', '').lower()
        last_name = data.get('last_name', '').lower()
        random_number = ''.join(random.choices(string.digits, k=4))
        username = f"{first_name}.{last_name}{random_number}"

        # Vérifier si le nom d'utilisateur est déjà utilisé
        while User.objects.filter(username=username).exists():
            random_number = ''.join(random.choices(string.digits, k=4))
            username = f"{first_name}.{last_name}{random_number}"

        parent = User(
            username=username,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone_number=data.get('phone_number', ''),
            address=data.get('address', ''),
            role=default_role,
            school_id=data.get('school'),
            gender=data.get('gender')  # Si le genre est pertinent pour les parents
        )

        # Gestion de l'image de profil
        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            parent.profile_picture = profile_picture

        # Gestion du mot de passe
        password = data.get('password')
        if password:
            parent.set_password(password)
        else:
            parent.set_unusable_password()

        parent.save()

        return Response(
            {'message': 'Parent créé avec succès.', 'parent': UserSerializer(parent).data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def retrieve_student(self, request, pk=None):
        try:
            student = User.objects.get(pk=pk, role__name='Étudiant')
            serializer = UserSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "Étudiant non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])
    def retrieve_parent(self, request, pk=None):
        try:
            parent = User.objects.get(pk=pk, role__id=4)
            serializer = UserSerializer(parent)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "¨Parent non trouvé."}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def retrieve_admin(self, request, pk=None):
        try:
            admin = User.objects.get(pk=pk, role__id=1)
            serializer = UserSerializer(admin)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "admin non trouvé."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put', 'patch'])
    def updatestudent(self, request, pk=None):
        try:
            student = User.objects.get(pk=pk, role__name='Étudiant')  # Trouver l'étudiant
        except User.DoesNotExist:
            raise NotFound("Étudiant introuvable.")  # Gérer le cas où l'étudiant n'existe pas

        data = request.data

        # Mettre à jour les champs de l'étudiant si fournis
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.email = data.get('email', student.email)
        student.phone_number = data.get('phone_number', student.phone_number)
        student.address = data.get('address', student.address)
        student.school_id = data.get('school', student.school_id)
        student.education_level_id = data.get('education_level', student.education_level_id)

        # Mise à jour du parent
        parent_id = data.get('parent', None)
        if parent_id == "null":  # Si la valeur est la chaîne "null", on la convertit en None
            parent_id = None

        if parent_id:
            try:
                parent = User.objects.get(pk=parent_id, role__name='Parent')  # Vérifier que le parent existe
                student.parent = parent
            except User.DoesNotExist:
                return Response({"detail": "Parent non trouvé."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            student.parent = None  # Si aucun parent n'est fourni ou valide, dissocier

        # Mise à jour du statut de paiement
        paid = data.get('paid', student.paid)
        if isinstance(paid, str):
            paid = paid.lower() in ['true', '1', 't', 'y', 'yes']
        student.paid = paid

        # Mettre à jour le service de transport
        transportation_service = data.get('transportation_service', student.transportation_service)
        if isinstance(transportation_service, str):
            transportation_service = transportation_service.lower() in ['true', '1', 't', 'y', 'yes']
        student.transportation_service = transportation_service

        # Mettre à jour le nombre d'absences et le paiement mensuel
        student.absences_number = data.get('absences_number', student.absences_number)
        student.monthly_payment = data.get('monthly_payment', student.monthly_payment)

        # # Mise à jour de la date du prochain paiement
        # next_payment_date = data.get('next_payment_date', None)
        # if next_payment_date and next_payment_date.lower() != "null":  # Vérifier et ignorer "null" comme chaîne
        #     student.next_payment_date = next_payment_date
        # else:
        #     student.next_payment_date = None  # Définir explicitement à None en cas d'absence

        # Mettre à jour la remarque (champ remark)
        student.remark = data.get('remark', student.remark)

        # Gestion de l'image de profil (optionnel)
        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            student.profile_picture = profile_picture

        # Mettre à jour le mot de passe si fourni
        password = data.get('password', None)
        if password:
            student.set_password(password)

        try:
            student.save()
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                'message': 'Étudiant mis à jour avec succès.',
                'profile_picture': student.profile_picture.url if student.profile_picture else None,
                'student': UserSerializer(student).data,
            },
            status=status.HTTP_200_OK
        )


    

    @action(detail=True, methods=['put', 'patch'])
    def updateparent(self, request, pk=None):
        try:
            parent = User.objects.get(pk=pk, role__name='Parent')  # Trouver l'étudiant
        except User.DoesNotExist:
            raise NotFound("Parent introuvable.")  # Gérer le cas où l'étudiant n'existe pas

        data = request.data

        # Mettre à jour les champs de l'étudiant si fournis
        parent.first_name = data.get('first_name', parent.first_name)
        parent.last_name = data.get('last_name', parent.last_name)
        parent.email = data.get('email', parent.email)
        parent.phone_number = data.get('phone_number', parent.phone_number)
        parent.address = data.get('address', parent.address)
        parent.school_id = data.get('school', parent.school_id)
        parent.education_level_id = data.get('education_level', parent.education_level_id)

        # Mise à jour du statut de paiement
        paid = data.get('paid', parent.paid)
        if isinstance(paid, str):
            paid = paid.lower() in ['true', '1', 't', 'y', 'yes']
        parent.paid = paid

        # Mettre à jour le service de transport
        transportation_service = data.get('transportation_service',parent.transportation_service)
        if isinstance(transportation_service, str):
            transportation_service = transportation_service.lower() in ['true', '1', 't', 'y', 'yes']
        parent.transportation_service = transportation_service

        # Mettre à jour le nombre d'absences et le paiement mensuel
        parent.absences_number = data.get('absences_number', parent.absences_number)
        parent.monthly_payment = data.get('monthly_payment', parent.monthly_payment)

        # # Mise à jour de la date du prochain paiement
        # next_payment_date = data.get('next_payment_date', None)
        # if next_payment_date and next_payment_date.lower() != "null":  # Vérifier et ignorer "null" comme chaîne
        #     parent.next_payment_date = next_payment_date
        # else:
        #     parent.next_payment_date = None  # Définir explicitement à None en cas d'absence

        # Gestion de l'image de profil (optionnel)
        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            parent.profile_picture = profile_picture

        # Mettre à jour le mot de passe si fourni
        password = data.get('password', None)
        if password:
            parent.set_password(password)

        try:
            parent.save()
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                'message': 'Parent mis à jour avec succès.',
                'profile_picture': parent.profile_picture.url if parent.profile_picture else None,
                'teacher': UserSerializer(parent).data,
            },
            status=status.HTTP_200_OK
        )


    @action(detail=True, methods=['delete'])
    def delete_student(self, request, pk=None):
        try:
            student = User.objects.get(pk=pk, role__id=2)  # Chercher l'étudiant par ID
            student.delete()  # Supprimer l'étudiant
            return Response({"detail": "Étudiant supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "Étudiant non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['delete'])
    def delete_parent(self, request, pk=None):
        try:
            student = User.objects.get(pk=pk, role__id=4)  # Chercher l'étudiant par ID
            student.delete()  # Supprimer l'étudiant
            return Response({"detail": "Parent supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "Parent non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        
    # CRUD pour les enseignants
    @action(detail=False, methods=['post'])
    def create_teacher(self, request):
        data = request.data
        default_role, created = Role.objects.get_or_create(name='Enseignant')

        # Générer un nom d'utilisateur unique
        first_name = data.get('first_name', '').lower()
        last_name = data.get('last_name', '').lower()
        random_number = ''.join(random.choices(string.digits, k=4))
        username = f"{first_name}.{last_name}{random_number}"

        # Vérifier si le username est déjà utilisé
        while User.objects.filter(username=username).exists():
            random_number = ''.join(random.choices(string.digits, k=4))
            username = f"{first_name}.{last_name}{random_number}"

        # Récupérer l'instance du sujet à partir de l'ID
        subject_id = data.get('subject')
        if subject_id:
            try:
                subject_instance = Subject.objects.get(id=subject_id)
            except Subject.DoesNotExist:
                return Response(
                    {"detail": "Le sujet spécifié n'existe pas."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            subject_instance = None

        # Créer l'enseignant avec l'instance du sujet
        teacher = User(
            username=username,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone_number=data.get('phone_number', ''),
            address=data.get('address', ''),
            role=default_role,
            school_id=data.get('school'),
            education_level_id=data.get('education_level'),
            subject=subject_instance,  # Assigner l'instance du sujet ici
        )

        # Gestion de l'image de profil
        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            print(f"Fichier 'profile_picture' reçu : {profile_picture.name}")
            teacher.profile_picture = profile_picture

        # Gestion du mot de passe
        password = data.get('password')
        if password:
            teacher.set_password(password)  # Hachage du mot de passe
            print(f"Mot de passe haché pour {teacher.email}: {teacher.password}")  # Vérifiez si le mot de passe est bien haché
        else:
            teacher.set_unusable_password()

        teacher.save()  # Sauvegarder l'utilisateur après avoir défini le mot de passe

        Course.objects.create(
            education_level=teacher.education_level,
            subject=teacher.subject,
            school=teacher.school,
            teacher=teacher,
        )

        return Response(
            {'message': 'Enseignant créé avec succès.', 'teacher': UserSerializer(teacher).data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'])
    def create_driver(self, request):
        data = request.data
        default_role, created = Role.objects.get_or_create(name='Chauffeur')

        # Générer un nom d'utilisateur unique
        first_name = data.get('first_name', '').lower()
        last_name = data.get('last_name', '').lower()
        random_number = ''.join(random.choices(string.digits, k=4))
        username = f"{first_name}.{last_name}{random_number}"

        # Vérifier si le nom d'utilisateur est déjà utilisé
        while User.objects.filter(username=username).exists():
            random_number = ''.join(random.choices(string.digits, k=4))
            username = f"{first_name}.{last_name}{random_number}"

        # Récupérer l'instance du sujet, si fournie
        subject_id = data.get('subject')
        if subject_id:
            try:
                subject_instance = Subject.objects.get(id=subject_id)
            except Subject.DoesNotExist:
                return Response(
                    {"detail": "Le sujet spécifié n'existe pas."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            subject_instance = None

        # Créer le chauffeur
        driver = User(
            username=username,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone_number=data.get('phone_number', ''),
            address=data.get('address', ''),
            role=default_role,
            school_id=data.get('school'),
            subject=subject_instance  # Assigner l'instance du sujet
        )

        # Gestion de l'image de profil (optionnelle)
        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            driver.profile_picture = profile_picture

        # Gestion du mot de passe
        password = data.get('password')
        if password:
            driver.set_password(password)
        else:
            driver.set_unusable_password()

        driver.save()

        return Response(
            {'message': 'Chauffeur créé avec succès.', 'driver': UserSerializer(driver).data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def retrieve_teacher(self, request, pk=None):
        teacher = get_object_or_404(User, pk=pk, role__name='Enseignant')
        serializer = UserSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def retrieve_driver(self, request, pk=None):
        try:
            driver = User.objects.get(pk=pk, role__id=5)
            serializer = UserSerializer(driver)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "Chauffeur non trouvé."}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['put', 'patch'])
    def update_teacher(self, request, pk=None):
        teacher = get_object_or_404(User, pk=pk, role__name='Enseignant')
        data = request.data

        # Mettre à jour les champs de l'enseignant si fournis
        teacher.first_name = data.get('first_name', teacher.first_name)
        teacher.last_name = data.get('last_name', teacher.last_name)
        teacher.email = data.get('email', teacher.email)
        teacher.phone_number = data.get('phone_number', teacher.phone_number)
        teacher.address = data.get('address', teacher.address)
        teacher.school_id = data.get('school', teacher.school_id)
        teacher.education_level_id = data.get('education_level', teacher.education_level_id)

        # Mise à jour du statut de paiement
        teacher.paid = bool(data.get('paid', teacher.paid))  # Ajout ici

        # Mettre à jour le nombre d'absences et les salaires
        teacher.absences_number = data.get('absences_number', teacher.absences_number)
        teacher.monthly_salary = data.get('monthly_salary', teacher.monthly_salary)
        teacher.session_salary = data.get('session_salary', teacher.session_salary)

        # next_payment_date = data.get('next_payment_date', None)
        # if next_payment_date:
        #     teacher.next_payment_date = next_payment_date

        # Récupérer l'instance du sujet à partir de l'ID, si fourni
        subject_id = data.get('subject', None)
        if subject_id is not None:  # Modifier uniquement si 'subject' est dans les données
            if subject_id:  # ID fourni, mettre à jour le sujet
                try:
                    subject_instance = Subject.objects.get(id=subject_id)
                except Subject.DoesNotExist:
                    return Response(
                        {"detail": "Le sujet spécifié n'existe pas."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                teacher.subject = subject_instance
            else:  # Réinitialiser le sujet à None si explicitement indiqué
                teacher.subject = None

        # Gestion de l'image de profil (optionnel)
        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            teacher.profile_picture = profile_picture

        # Mettre à jour le mot de passe si fourni
        password = data.get('password', None)
        if password:
            teacher.set_password(password)

        teacher.save()

        return Response(
            {
                'message': 'Enseignant mis à jour avec succès.',
                'profile_picture': teacher.profile_picture.url if teacher.profile_picture else None,
                'teacher': UserSerializer(teacher).data,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['put', 'patch'])
    def update_admin(self, request, pk=None):
        admin = get_object_or_404(User, pk=pk, role__name='Administrateur')
        data = request.data

        # Mettre à jour les champs de l'administrateur si fournis
        admin.first_name = data.get('first_name', admin.first_name)
        admin.last_name = data.get('last_name', admin.last_name)
        admin.email = data.get('email', admin.email)
        admin.phone_number = data.get('phone_number', admin.phone_number)
        admin.address = data.get('address', admin.address)
        admin.school_id = data.get('school', admin.school_id)

        # Gestion de l'image de profil (optionnel)
        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            print(f"Fichier reçu : {profile_picture.name}")
            admin.profile_picture = profile_picture

        # Mettre à jour le mot de passe si fourni
        password = data.get('password', None)
        if password:
            admin.set_password(password)

        admin.save()

        return Response(
            {
                'message': 'Administrateur mis à jour avec succès.',
                'profile_picture': admin.profile_picture.url if admin.profile_picture else None,
                'admin': UserSerializer(admin).data,
            },
            status=status.HTTP_200_OK
        )


    @action(detail=True, methods=['delete'])
    def delete_teacher(self, request, pk=None):
        teacher = get_object_or_404(User, pk=pk, role__name='Enseignant')
        teacher.delete()
        return Response({"detail": "Enseignant supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)  
    
    @action(detail=True, methods=['patch'], url_path='mark-paid')
    def mark_paid(self, request, pk=None):
        try:
            print(f"ID reçu pour la mise à jour : {pk}")
            teacher = get_object_or_404(User, pk=pk)
        
            teacher.paid = True
            teacher.save()

            # Créer une transaction associée
            print("Création de la transaction...")
            transaction = Transaction.objects.create(
                type='expense',
                amount=teacher.monthly_salary,
                description=f"Salaire payé à {teacher.first_name} {teacher.last_name}",
                school=teacher.school,
            )
            print(f"Transaction créée : {transaction.id}")

            return Response({"message": "Statut de paiement mis à jour et transaction enregistrée."}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Erreur lors de la mise à jour : {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
    @action(detail=True, methods=['patch'], url_path='mark-student-paid')
    def mark_student_paid(self, request, pk=None):
        try:
            print(f"ID reçu pour la mise à jour : {pk}")
            student = get_object_or_404(User, pk=pk)
            if not student.paid:
                student.paid = True
                student.save()

                # Créer une transaction associée
                Transaction.objects.create(
                    type='earning',
                    amount=student.monthly_payment,
                    description=f"Montant mensuel payé par {student.first_name} {student.last_name}",
                    school=student.school,
                )

            return Response({"message": "Statut de paiement mis à jour et transaction enregistrée."}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Erreur lors de la mise à jour : {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='mark-driver-paid')
    def mark_driver_paid(self, request, pk=None):
        try:
            driver = get_object_or_404(User, pk=pk)
            is_paid = request.data.get("paid", False)  # Get 'paid' from request data

            print(f"Request data: {request.data}")  # Log the entire request data
            print(f"is_paid: {is_paid}")  # Log the value of 'is_paid'

            if is_paid:
                # Mark as paid and create an expense transaction
                if not driver.paid:  # Only if not already paid
                    print(f"Marking driver {driver.first_name} {driver.last_name} as paid.")
                    driver.paid = True
                    driver.save()

                    print(f"Creating transaction for driver {driver.first_name} {driver.last_name}")
                    transaction = Transaction.objects.create(
                        type='expense',
                        amount=driver.monthly_salary,
                        description=f"Salaire payé au chauffeur {driver.first_name} {driver.last_name}",
                        school=driver.school,
                    )
                    print(f"Transaction created: {transaction.id}, amount: {transaction.amount}")
            else:
                # Mark as unpaid
                print(f"Marking driver {driver.first_name} {driver.last_name} as unpaid.")
                driver.paid = False
                driver.save()

            return Response({"message": "Statut de paiement mis à jour."}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error during mark_driver_paid: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def calculate_coefficients_sum(self, request, pk=None):
        """
        Retourner uniquement la somme des coefficients des matières d'un étudiant.
        """
        try:
            # Récupérer l'étudiant
            student = self.get_object()

            # Vérifier que l'étudiant a un niveau d'éducation
            if not student.education_level:
                return Response(
                    {"error": "L'étudiant n'a pas de niveau d'éducation attribué."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Récupérer les matières associées au niveau d'éducation
            subjects = Subject.objects.filter(education_level=student.education_level)

            # Calculer la somme des coefficients
            coefficients_sum = subjects.aggregate(total=Sum('coefficient'))['total'] or 0

            # Retourner uniquement la somme des coefficients
            return Response(coefficients_sum, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def calculate_general_average(self, request, pk=None):
        """
        Calculer la moyenne générale de l'étudiant.
        """
        try:
            # Récupérer l'étudiant
            student = self.get_object()

            # Vérifier que l'étudiant a un niveau d'éducation
            if not student.education_level:
                return Response(
                    {"error": "L'étudiant n'a pas de niveau d'éducation attribué."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Récupérer les matières associées
            subjects = Subject.objects.filter(education_level=student.education_level)

            # Récupérer les coefficients pour ces matières
            coefficients = subjects.values_list('id', 'coefficient')

            # Récupérer les notes finales de l'étudiant
            grades = Grade.objects.filter(student=student, subject__in=subjects)

            # Calculer la somme des coefficients
            total_coefficients = subjects.aggregate(total=Sum('coefficient'))['total'] or 0

            # Calculer la somme pondérée des notes finales
            weighted_sum = 0
            for subject_id, coefficient in coefficients:
                subject_grades = grades.filter(subject_id=subject_id)
                if subject_grades.exists():
                    # Calculer la note finale pour la matière
                    total_grade = sum([grade.score for grade in subject_grades])
                    final_grade = total_grade / len(subject_grades) if len(subject_grades) > 0 else 0
                    weighted_sum += final_grade * (coefficient or 1)  # Utiliser 1 si le coefficient est null

            # Calculer la moyenne générale
            general_average = weighted_sum / total_coefficients if total_coefficients > 0 else 0

            return Response({
                "general_average": round(general_average, 2),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
def dashboard_summary(request):

    school_id = request.GET.get('school_id')
    
    if not school_id:
        return Response(
            {"error": "Aucun ID d'école trouvé dans les paramètres de la requête."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    students_count = User.objects.filter(role__name="Étudiant", school__id=school_id).count()
    teachers_count = User.objects.filter(role__name="Enseignant", school__id=school_id).count()
    drivers_count = User.objects.filter(role__name="Chauffeur", school__id=school_id).count()
    parents_count = User.objects.filter(role__name="Parent", school__id=school_id).count()

    male_students_count = User.objects.filter(role__name="Étudiant", gender="MALE",school__id = school_id).count()
    female_students_count = User.objects.filter(role__name="Étudiant", gender="FEMALE",school__id = school_id).count()

    data = {
        "students_count": students_count,
        "teachers_count": teachers_count,
        "drivers_count": drivers_count,
        "parents_count": parents_count,
        "male_students_count": male_students_count,
        "female_students_count": female_students_count,
    }
    return Response(data)
            
@api_view(['GET'])
def fetch_schools(request):
    # Récupérer toutes les écoles distinctes des utilisateurs
    schools = User.objects.values_list('school', flat=True).distinct()
    return Response(schools)

    
class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return Response({'error': 'Token manquant.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            print(f"User ID extrait : {user_id}")
            user = User.objects.get(id=user_id)
            
            if not user.is_verified:
                user.is_verified = True
                user.save()
                print(f"Email vérifié pour l'utilisateur : {user.email}")
                return Response({'message': 'Email vérifié avec succès !'}, status=status.HTTP_200_OK)
            else:
                print(f"L'email a déjà été vérifié pour l'utilisateur : {user.email}")
                return Response({'message': 'Email déjà vérifié.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'error': 'Token invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = str(RefreshToken.for_user(user).access_token)
            send_reset_password_email(user, token)
            return Response({'message': 'Un email de réinitialisation a été envoyé.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé avec cet email.'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            # Valider le token et obtenir l'utilisateur
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)

            # Mettre à jour le mot de passe
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class SendSMSView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        message = request.data.get('message', 'Voici un SMS de démonstration.')

        if not phone_number:
            return Response({'error': 'Numéro de téléphone manquant.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Envoi du SMS via Twilio
            response_sid = send_sms(user=None, phone_number=phone_number, message=message)
            return Response({
                'message': 'SMS envoyé avec succès.',
                'twilio_message_sid': response_sid  # Renvoi de l'ID du message pour le suivi
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Erreur lors de l\'envoi du SMS : {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def education_levels_by_school(request, school_id):
    levels = EducationLevel.objects.filter(school_id=school_id)
    serializer = EducationLevelSerializer(levels, many=True)
    return Response(serializer.data)



class EventViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing event instances.
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        if not school_id:
            return Event.objects.none()
        return Event.objects.filter(school_id=school_id).order_by('date')

    def create(self, request, *args, **kwargs):
        print("Données reçues dans la requête :", request.data)
        school_id = request.data.get('school')
        if not school_id:
            return Response({"error": "Le champ 'school' est requis."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['delete'], url_path='delete-today')
    def delete_today(self, request, *args, **kwargs):
        """
        Deletes all events scheduled for today.
        """
        school_id = request.query_params.get('school_id')
        if not school_id:
            return Response({"error": "Le paramètre 'school_id' est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        today = date.today()
        events_to_delete = Event.objects.filter(school_id=school_id, date=today)

        if not events_to_delete.exists():
            return Response({"message": "Aucun événement trouvé pour aujourd'hui."}, status=status.HTTP_404_NOT_FOUND)

        count = events_to_delete.count()
        events_to_delete.delete()
        return Response({"message": f"{count} événement(s) supprimé(s) pour aujourd'hui."}, status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        print("Données reçues dans la requête :", request.data)  # Log les données de la requête
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        if school_id is not None:
            return Transaction.objects.filter(school_id=school_id)
        return super().get_queryset()
    
    @action(detail=False, methods=['get'], url_path='expenses')
    def get_expenses(self, request):
        school_id = request.query_params.get('school_id')
        if school_id is None:
            return Response({"error": "school_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        expenses = Transaction.objects.filter(school_id=school_id, type='expense')
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='earnings')
    def get_earnings(self, request):
        school_id = request.query_params.get('school_id')
        if school_id is None:
            return Response({"error": "school_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        earnings = Transaction.objects.filter(school_id=school_id, type='earning')
        serializer = self.get_serializer(earnings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create-expense')
    def create_expense(self, request):
        school_id = request.data.get('school')
        if not school_id:
            return Response({"error": "school field is required"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['type'] = 'expense'  # Forcer le type à "expense"
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='create-earning')
    def create_earning(self, request):
        school_id = request.data.get('school')
        if not school_id:
            return Response({"error": "school field is required"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['type'] = 'earning'  # Forcer le type à "earning"
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'], url_path='monthly')
    def monthly(self, request):
        school_id = request.query_params.get('school_id')
        
        # Filtrer par école si `school_id` est fourni
        queryset = self.queryset
        if school_id is not None:
            queryset = queryset.filter(school_id=school_id)

        # Agréger les transactions par mois et calculer le montant total
        monthly_data = queryset.annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')

        # Formater la réponse pour un meilleur affichage
        formatted_data = [
            {
                "month": entry["month"].strftime("%B %Y"),  # Par exemple : "April 2021"
                "amount": entry["total_amount"]
            }
            for entry in monthly_data
        ]
        return Response(formatted_data)

    @action(detail=False, methods=['get'], url_path='monthly-expenses')
    def monthly_expenses(self, request):
        school_id = request.query_params.get('school_id')
        
        # Filtrer par école et par type de transaction 'expense'
        queryset = self.queryset.filter(type='expense')
        if school_id is not None:
            queryset = queryset.filter(school_id=school_id)

        # Agréger les dépenses par mois
        monthly_data = queryset.annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')

        # Formater la réponse pour un meilleur affichage
        formatted_data = [
            {
                "month": entry["month"].strftime("%B %Y"),
                "amount": entry["total_amount"]
            }
            for entry in monthly_data
        ]
        return Response(formatted_data)

    @action(detail=False, methods=['get'], url_path='monthly-earnings')
    def monthly_earnings(self, request):
        school_id = request.query_params.get('school_id')
        
        # Filtrer par école et par type de transaction 'earning'
        queryset = self.queryset.filter(type='earning')
        if school_id is not None:
            queryset = queryset.filter(school_id=school_id)

        # Agréger les revenus par mois
        monthly_data = queryset.annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')

        # Formater la réponse pour un meilleur affichage
        formatted_data = [
            {
                "month": entry["month"].strftime("%B %Y"),
                "amount": entry["total_amount"]
            }
            for entry in monthly_data
        ]
        return Response(formatted_data)

@api_view(['POST'])
def verify_secret_key(request):
    secret_key = request.data.get('secret_key')
    try:
        student = User.objects.get(parent_key=secret_key)
        return Response({'success': True, 'student_id': student.id}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'success': False, 'message': 'Clé secrète invalide.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_student_info(request):
    secret_key = request.GET.get('secret_key')
    try:
        student = User.objects.get(parent_key=secret_key)
        serializer = UserSerializer(student)
        return Response({'success': True, 'student': serializer.data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'success': False, 'message': 'Clé secrète invalide.'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_timetable_by_parent_key(request, parent_key):
    try:
        # Trouver l'étudiant associé à la parent_key
        student = User.objects.get(parent_key=parent_key, role__name="Étudiant")
        
        # Filtrer les sessions d'emploi du temps pour l'étudiant
        timetable_sessions = TimetableSession.objects.filter(
            education_level=student.education_level, school=student.school
        )
        
        # Sérialiser les données
        data = list(timetable_sessions.values(
            'day', 'start_time', 'end_time', 
            'subject__name', 'teacher__first_name', 'teacher__last_name', 
            'classroom__name'
        ))
        return JsonResponse({'status': 'success', 'timetable': data, 'student_name': f"{student.first_name} {student.last_name}"})
    
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Clé parent invalide ou étudiant introuvable.'})



def get_education_level_by_parent_key(request, parent_key):
    from urllib.parse import unquote
    try:
        # Décodage de la clé parent si elle est encodée
        decoded_key = unquote(parent_key)
        
        # Recherche de l'étudiant associé à la clé parent
        student = User.objects.get(parent_key=decoded_key, role__name='Étudiant')
        
        # Retourner uniquement l'ID du niveau d'éducation
        return JsonResponse({'education_level_id': student.education_level.id})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Clé parent invalide ou étudiant introuvable.'}, status=404)

def get_school_by_parent_key(request, parent_key):
    from urllib.parse import unquote
    try:
        # Décodage de la clé parent si elle est encodée
        decoded_key = unquote(parent_key)
        
        # Recherche de l'étudiant associé à la clé parent
        student = User.objects.get(parent_key=decoded_key, role__name='Étudiant')
        
        # Retourner uniquement l'ID du niveau d'éducation
        return JsonResponse({'school_id': student.school.id})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Clé parent invalide ou étudiant introuvable.'}, status=404)

def get_student_by_parent_key(request, parent_key):
    from urllib.parse import unquote
    try:
        # Décodage de la clé parent si elle est encodée
        decoded_key = unquote(parent_key)
        
        # Recherche de l'étudiant associé à la clé parent
        student = User.objects.get(parent_key=decoded_key, role__name='Étudiant')
        
        # Retourner uniquement l'ID du niveau d'éducation
        return JsonResponse({'student_id': student.id})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Clé parent invalide ou étudiant introuvable.'}, status=404)

def get_absences_by_parent_key(request, parent_key):
    from urllib.parse import unquote
    try:
        # Décodage de la clé parent si elle est encodée
        decoded_key = unquote(parent_key)
        
        # Recherche de l'étudiant associé à la clé parent
        student = User.objects.get(parent_key=decoded_key, role__name='Étudiant')
        
        # Retourner uniquement l'ID du niveau d'éducation
        return JsonResponse({'absences_number': student.absences_number})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Clé parent invalide ou étudiant introuvable.'}, status=404)


def get_stations_by_driver_id(request,driver_id):
    from urllib.parse import unquote
    try:
        # Décodage de la clé parent si elle est encodée
        decoded_key = unquote(driver_id)
        
        # Recherche de l'étudiant associé à la clé parent
        transport = Transport.objects.get(driver_id=decoded_key)
        
        # Retourner uniquement l'ID du niveau d'éducation
        return JsonResponse({'transport_id': transport.id})
    except User.DoesNotExist:
        return JsonResponse({'error': 'id du transport ou chauffeur introuvable.'}, status=404)


def get_teachers_by_subject(request, subject_id):
    from urllib.parse import unquote
    try:
        # Décodage de la clé parent si elle est encodée
        decoded_key = unquote(subject_id)
        
        # Recherche des enseignants associés au sujet
        teachers = User.objects.filter(subject_id=decoded_key, role__name='Enseignant')
        
        # Si aucun enseignant n'est trouvé
        if not teachers.exists():
            return JsonResponse({'error': 'Aucun enseignant trouvé pour ce sujet.'}, status=404)

        # Construire une liste des enseignants
        teacher_list = [{'id': teacher.id, 'name': f"{teacher.first_name} {teacher.last_name}"} for teacher in teachers]
        
        # Retourner la liste des enseignants
        return JsonResponse({'teachers': teacher_list})
    except Exception as e:
        return JsonResponse({'error': f"Une erreur est survenue: {str(e)}"}, status=500)
    
class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

    def get_queryset(self):

        queryset = self.queryset
        school_id = self.request.query_params.get('school_id')

        if school_id:
            queryset = queryset.filter(school_id=school_id)

        return queryset
    
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        # Récupérer les paramètres de requête pour vérifier une chatroom entre deux utilisateurs
        user1 = self.request.query_params.get('user1')
        user2 = self.request.query_params.get('user2')

        if user1 and user2:
            # Vérifier si une chatroom existe entre user1 et user2
            return self.queryset.filter(
                Q(user1_id=user1, user2_id=user2) | Q(user1_id=user2, user2_id=user1)
            )
        return self.queryset
    
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Filtrer les notifications pour l'utilisateur authentifié
        return self.queryset.filter(user=self.request.user).order_by('-created_at')
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        chatroom_id = self.request.query_params.get('chat_room')
        if chatroom_id:
            return self.queryset.filter(chat_room_id=chatroom_id)
        return self.queryset.none()


    def create(self, request, *args, **kwargs):
        # Créer le message
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()  # Sauvegarder le message et obtenir l'instance

        # Déterminer le destinataire
        chat_room = message.chat_room
        if message.sender == chat_room.user1:
            recipient = chat_room.user2
        else:
            recipient = chat_room.user1

        # Créer une notification pour le destinataire
        Notification.objects.create(
            user=recipient,
            message=f"Vous avez reçu un message de {message.sender.first_name}  {message.sender.last_name}"
        )

        # Retourner la réponse avec le message créé
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)   


@api_view(['PATCH'])
def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.delete()  # Supprime la notification de la base de données
        return Response({"message": "Notification deleted successfully"}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@csrf_exempt
def upload_file(request):
    # Vérifier si une requête POST est faite
    if request.method == 'POST' and request.FILES.get('file'):
        # Récupérer le fichier envoyé avec la requête
        file = request.FILES['file']
        
        # Définir le chemin du fichier dans S3
        file_name = file.name
        
        # Utiliser le stockage par défaut pour télécharger sur S3
        file_path = default_storage.save(f'media/{file_name}', ContentFile(file.read()))
        
        # Générer l'URL du fichier téléchargé
        file_url = default_storage.url(file_path)

        return JsonResponse({"message": "File uploaded successfully", "file_url": file_url}, status=200)
    
    return JsonResponse({"message": "No file provided"}, status=400)



class DriverTransportsView(APIView):

    def get(self, request):
        user = request.user

        # Vérifier si l'utilisateur est un chauffeur
        if user.role.name != 'Chauffeur':
            return Response({"error": "Vous n'êtes pas autorisé à accéder à cette ressource."}, status=403)

        # Récupérer tous les transports liés au chauffeur
        transports = Transport.objects.filter(driver=user)

        # Retourner les IDs et les noms des transports
        transport_data = transports.values('id', 'name')

        return Response(transport_data, status=200)

class DeleteEventsByDate(APIView):
    """
    API endpoint to delete all events for a specific date.
    """
    def delete(self, request, *args, **kwargs):
        school_id = request.query_params.get('school_id')
        selected_date = request.query_params.get('date')  # Date à supprimer

        if not school_id:
            return Response({"error": "Le paramètre 'school_id' est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not selected_date:
            return Response({"error": "Le paramètre 'date' est requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convertir la date en objet datetime
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date() + timedelta(days=1)
        except ValueError:
            return Response({"error": "Le format de la date doit être 'YYYY-MM-DD'."}, status=status.HTTP_400_BAD_REQUEST)

        events_to_delete = Event.objects.filter(school_id=school_id, date=selected_date)

        if not events_to_delete.exists():
            return Response({"message": "Aucun événement trouvé pour cette date."}, status=status.HTTP_404_NOT_FOUND)

        count = events_to_delete.count()
        events_to_delete.delete()
        return Response({"message": f"{count} événement(s) supprimé(s) pour la date {selected_date}."}, status=status.HTTP_200_OK)
    


class DuplicateTeacherEducationLevelsView(APIView):
    """
    Vue pour récupérer les niveaux d'éducation associés aux enseignants dupliqués.
    """
    def get(self, request, *args, **kwargs):
        first_name = request.query_params.get('first_name')
        last_name = request.query_params.get('last_name')

        if not first_name or not last_name:
            return Response({"error": "Les paramètres 'first_name' et 'last_name' sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        # Récupérer les enseignants ayant le même prénom et nom
        duplicated_teachers = User.objects.filter(
            Q(first_name=first_name) & Q(last_name=last_name)
        ).values('id', 'first_name', 'last_name', 'education_level__id', 'education_level__name')

        return Response(list(duplicated_teachers), status=status.HTTP_200_OK)


class DuplicateTeacherSubjects(APIView):
    """
    Vue pour récupérer les niveaux d'éducation associés aux enseignants dupliqués.
    """
    def get(self, request, *args, **kwargs):
        first_name = request.query_params.get('first_name')
        last_name = request.query_params.get('last_name')

        if not first_name or not last_name:
            return Response({"error": "Les paramètres 'first_name' et 'last_name' sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        # Récupérer les enseignants ayant le même prénom et nom
        duplicated_teachers = User.objects.filter(
            Q(first_name=first_name) & Q(last_name=last_name)
        ).values('id', 'first_name', 'last_name', 'subject__id', 'subject__name')

        return Response(list(duplicated_teachers), status=status.HTTP_200_OK)
    
