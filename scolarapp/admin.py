from django.contrib import admin
from .models import Role,User,EducationLevel,School,Subject,Timetable,Transaction,Grade,Course,Event,Transport,Location,TransportLocation


# Register your models here.
admin.site.register(Role)
admin.site.register(User)
admin.site.register(EducationLevel)
admin.site.register(School)
admin.site.register(Timetable)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Transaction)
admin.site.register(Course)
admin.site.register(Event)
admin.site.register(Transport)
admin.site.register(Location)
admin.site.register(TransportLocation)