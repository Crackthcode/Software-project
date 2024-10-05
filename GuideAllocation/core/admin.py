from django.contrib import admin
from .models import Student, PreferenceList, Faculty, Clash, FinalAllotment, Deadline, Teacher, Student_log, Faculty_log

# Register your models here
admin.site.register(Student)
admin.site.register(PreferenceList)
admin.site.register(Faculty)
admin.site.register(Clash)
admin.site.register(FinalAllotment)
admin.site.register(Deadline)
admin.site.register(Teacher)
admin.site.register(Student_log)
admin.site.register(Faculty_log)