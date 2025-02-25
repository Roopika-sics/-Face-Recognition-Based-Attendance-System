from django.db import models

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student_photos/')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.student_name
