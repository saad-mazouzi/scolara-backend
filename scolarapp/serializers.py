from rest_framework import serializers
from .models import User,Role,EducationLevel,School,Classroom,Timetable,Subject,TimetableSession,Course,CourseFile,Grade,Transport,Location,TransportLocation,Event,Transaction,TeacherAvailability,Control,ChatRoom,Message,Notification,TimeSlot,Notice
from django.contrib.auth.hashers import make_password
import random
import string
from datetime import datetime

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields='__all__'

class TeacherAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model=TeacherAvailability
        fields = '__all__'

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields='__all__'

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
        
class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model= Classroom
        fields='__all__'

        
class TimetableSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableSession
        fields = '__all__'

class TimetableSerializer(serializers.ModelSerializer):
    sessions = TimetableSessionSerializer(many=True, read_only=True)  # Nested sessions

    class Meta:
        model = Timetable
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model= Subject
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'


class CourseFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseFile
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class TransportLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()  # Nested serializer to show location details

    class Meta:
        model = TransportLocation
        fields = ['transport', 'location', 'order']

class TransportSerializer(serializers.ModelSerializer):
    transport_locations = TransportLocationSerializer(many=True, read_only=True)  # Nested serializer for related locations
    students = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.filter(role__name='Étudiant'))

    class Meta:
        model = Transport
        fields = '__all__'

        
class UserSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'phone_number', 'address', 'email',
            'password', 'role', 'date_joined', 'is_verified', 'subject',
            'profile_picture', 'gender', 'school', 'education_level','absences_number','paid',
            'monthly_salary','session_salary', 'monthly_payment','transportation_service',
            'parent_key','remark','parent','children'
        ]
        extra_kwargs = {
            'password': {'required': False, 'write_only': True},  # Facultatif et non retourné
            'address': {'required': False, 'allow_blank': True},  # Facultatif, accepte ""
        }

    def get_parent(self, obj):
        """Récupérer les informations du parent en lecture seule."""
        if obj.parent:
            return {
                'id': obj.parent.id,
                'first_name': obj.parent.first_name,
                'last_name': obj.parent.last_name,
                'email': obj.parent.email,
                'phone_number': obj.parent.phone_number,
            }
        return None

    def create(self, validated_data):

        
        default_role, created = Role.objects.get_or_create(name='Étudiant')
        parent_data = validated_data.pop('parent', None)


        # Générer un nom d'utilisateur unique
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        random_number = ''.join(random.choices(string.digits, k=4))
        username = f"{first_name.lower()}.{last_name.lower()}{random_number}"

        # Créer l'utilisateur
        user = User(
            username=username,
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address', ''),  # Valeur par défaut ""
            role=validated_data.get('role', default_role),
            subject=validated_data.get('subject', None),
            profile_picture=validated_data.get('profile_picture', None),
            gender=validated_data.get('gender', None),
            school=validated_data.get('school', None),
            education_level=validated_data.get('education_level', None),
            remark=validated_data.get('remark', None),  # Inclure la remarque
            parent=parent_data  # Associer un parent s'il est fourni

        )
        print(user)

        # Vérifier si un mot de passe est fourni
        password = validated_data.get('password')
        if password:
            user.set_password(password)  # Chiffrer le mot de passe
        else:
            user.set_unusable_password()  # Générer un mot de passe inutilisable

        user.save()
        return user
    
    # def validate_next_payment_date(self, value):
    #     if value is None:
    #         return value
    #     try:
    #         # Valider le format de la date
    #         datetime.strptime(value, '%Y-%m-%d')
    #         return value
    #     except ValueError:
    #         raise serializers.ValidationError("La date doit être au format YYYY-MM-DD.")

    def update(self, instance, validated_data):
        # Gestion de la mise à jour du parent
        parent_data = validated_data.pop('parent', None)
        if parent_data:
            instance.parent_id = parent_data

        # Mise à jour des autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
    def get_children(self, obj):
        if obj.role and obj.role.name == "Parent":
            return [
                {"id": child.id, "first_name": child.first_name, "last_name": child.last_name}
                for child in obj.children.all()
            ]
        return []


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

class TimeSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSlot
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Grade
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'school']

    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'type', 'amount', 'date', 'description', 'school']

class ControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def validate(self, data):
        # Valider que soit un fichier, soit un contenu est présent
        if not data.get('content') and not data.get('file'):
            raise serializers.ValidationError('Un message texte ou un fichier est requis.')
        return data