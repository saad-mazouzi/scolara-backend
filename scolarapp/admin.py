from django.contrib import admin
from .models import Role,User,EducationLevel,School,Subject,Timetable,Transaction,Grade,Course,Event,Transport,Location,TransportLocation,Classroom,TeacherAvailability,TimetableSession,CourseFile,Control,ChatRoom,Message,Notification,TimeSlot,Notice


# Register your models here.
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Classroom)
admin.site.register(TeacherAvailability)
admin.site.register(EducationLevel)
admin.site.register(School)
admin.site.register(Timetable)
admin.site.register(TimetableSession)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Transaction)
admin.site.register(Course)
admin.site.register(CourseFile)
admin.site.register(Event)
admin.site.register(Transport)
admin.site.register(Location)
admin.site.register(TransportLocation)
admin.site.register(Control)
admin.site.register(ChatRoom)
admin.site.register(Message)    
admin.site.register(Notification)
admin.site.register(TimeSlot)
admin.site.register(Notice)
