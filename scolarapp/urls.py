from rest_framework.routers import DefaultRouter
from .views import UserViewSet,RoleViewset,VerifyEmailView,RequestPasswordResetView,PasswordResetConfirmView,fetch_schools,EducationLevelViewset,SchoolViewSet,education_levels_by_school,ClassroomViewset,TimetableViewSet,SubjectViewSet,TimetableSessionViewSet, GradeViewSet,dashboard_summary,EventViewSet,TransactionViewSet,verify_secret_key,get_student_info,TeacherAvailabilityViewset,ControlViewSet,get_education_level_by_parent_key,get_school_by_parent_key,get_student_by_parent_key,get_absences_by_parent_key,get_stations_by_driver_id,get_teachers_by_subject,ChatRoomViewSet,MessageViewSet, NotificationViewSet,NoticeViewSet,HomeworkBookViewSet
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TransportViewSet,LocationViewSet,TransportLocationViewSet
from .views import SchoolViewSet,CourseViewset,CourseFileViewset,SendSMSView, mark_notification_as_read , delete_notification , TimeSlotViewSet
from .views import upload_file,DriverTransportsView,DeleteEventsByDate,DuplicateTeacherEducationLevelsView,DuplicateTeacherSubjects

router = DefaultRouter()
router.register(r'roles',RoleViewset)
router.register(r'users',UserViewSet)
router.register(r'teacher-availability',TeacherAvailabilityViewset)
router.register(r'educationlevel',EducationLevelViewset)
router.register(r'school',SchoolViewSet)
router.register(r'classrooms',ClassroomViewset)
router.register(r'timetables', TimetableViewSet)
router.register(r'timetable-sessions', TimetableSessionViewSet)
router.register(r'subjects',SubjectViewSet)
router.register(r'course',CourseViewset)
router.register(r'coursefile',CourseFileViewset)
router.register(r'grades',GradeViewSet)
router.register(r'transports', TransportViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'transports-locations', TransportLocationViewSet)
router.register(r'events', EventViewSet, basename='event')
router.register(r'transactions', TransactionViewSet)
router.register(r'controls',ControlViewSet)
router.register(r'chatrooms', ChatRoomViewSet, basename='chat-room')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications' , NotificationViewSet , basename='notification')
router.register(r'timeslots', TimeSlotViewSet, basename='timeslot')
router.register(r'notices', NoticeViewSet, basename='notice')
router.register(r'homework-books', HomeworkBookViewSet, basename='homework-book')



urlpatterns = [
    path('api/',include(router.urls)),
    path('api/schools/', fetch_schools, name='fetch_schools'),
    path('api/dashboard/', dashboard_summary, name='dashboard_summary'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/password-reset/', RequestPasswordResetView.as_view(), name='password-reset'),
    path('api/send-sms/', SendSMSView.as_view(), name='send-sms'),
    path('api/verify-secret-key/', verify_secret_key, name='verify_secret_key'),
    path('api/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('education-levels/<int:school_id>/', education_levels_by_school, name='education_levels_by_school'),
    path('api/student-info/', get_student_info, name='get_student_info'),
    path('api/education-level-by-parent-key/<str:parent_key>/', get_education_level_by_parent_key, name='education-level-by-parent-key'),
    path('api/school-by-parent-key/<str:parent_key>/', get_school_by_parent_key, name='school-by-parent-key'),
    path('api/student-by-parent-key/<str:parent_key>/', get_student_by_parent_key, name='student-by-parent-key'),
    path('api/absences-by-parent-key/<str:parent_key>/', get_absences_by_parent_key, name='absences-by-parent-key'),
    path('api/stations-by-driver-id/<str:driver_id>/', get_stations_by_driver_id, name='stations-by-driver-id'),
    path('api/teacher-by-subject/<str:subject_id>/', get_teachers_by_subject, name='teacher-by-subject'),
    path('notifications/<int:notification_id>/read/', mark_notification_as_read, name='mark-notification-as-read'),
    path('notifications/<int:notification_id>/', delete_notification, name='delete-notification'),
    path('upload/', upload_file, name='upload_file'),
    path('api/driver-transports/', DriverTransportsView.as_view(), name='driver-transports'),
    path('events/delete-by-date/', DeleteEventsByDate.as_view(), name='delete_events_by_date'),
    path('api/duplicate-teacher-education-levels/', DuplicateTeacherEducationLevelsView.as_view(), name='duplicate-teacher-education-levels'),
    path('api/duplicate-teacher-subjects/', DuplicateTeacherSubjects.as_view(), name='duplicate-teacher-subjects'),

]


