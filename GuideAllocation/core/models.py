from django.db import models
import json
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets

#========================================AUTHORISATION===================================================
   




#=======================================STUDENT==================================================
class Student(models.Model):
    student_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    email = models.CharField(max_length=255)
    is_eligible=models.BooleanField(default=False)
    def __str__(self):
        return self.name

class PreferenceList(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    preferences = models.TextField()  

    def set_preferences(self, preferences):
        self.preferences = json.dumps(preferences)

    def get_preferences(self):
        return json.loads(self.preferences)
    
#=======================================FACULTY==================================================
class Faculty(models.Model):
    teacher_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default='studentmail.sid0+DN@gmail.com')
    willingness = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
#=======================================ADMINISTARTOR================================================
class Clash(models.Model):
    faculty_name = models.CharField(max_length=255)
    cluster_number = models.IntegerField()
    students = models.TextField()  
    chosen_student = models.CharField(max_length=255, default="nobody")  # Add this field

    def set_students(self, students):
        self.students = json.dumps(students)

    def get_students(self):
        return json.loads(self.students)

class FinalAllotment(models.Model):
    student_roll_no = models.CharField(max_length=255)
    faculty_name = models.CharField(max_length=255)
    cluster_number = models.IntegerField()

class Deadline(models.Model):
    student_deadline = models.DateTimeField()
    faculty_deadline = models.DateTimeField()
#=======================================REPORT==================================================  
class Teacher(models.Model):
    teacher_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return self.name

#=======================================LOG FILES==================================================

class Student_log(models.Model):
    student_name = models.CharField(max_length=64)
    student_rollno = models.CharField(max_length=8, unique=True)  
    student_log = models.FileField(upload_to='logfiles/students_logs/', null=True)

class Faculty_log(models.Model):
    faculty_name = models.CharField(max_length=64)
    faculty_id = models.IntegerField(unique=True) 
    faculty_log = models.FileField(upload_to='logfiles/faculty_logs/', null=True)


    




