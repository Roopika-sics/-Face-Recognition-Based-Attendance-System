from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student_photos/')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    
    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['username', 'student_name', 'student_id', 'department']
    
    def __str__(self):
        return self.username
