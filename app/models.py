from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.contrib import messages

class FacultyManager(models.Manager):
    def create_faculty(self, faculty_id, email, password=None):
        if not faculty_id:
            raise ValueError("Faculty ID is required")
        if not email:
            raise ValueError("Email is required")

        faculty = self.model(faculty_id=faculty_id, email=email)
        if password:
            faculty.set_password(password)
        faculty.save(using=self._db)
        return faculty

class Faculty(models.Model):
    faculty_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    faculty_name = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=128)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = FacultyManager()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.faculty_id
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default="#337BFF")

    def __str__(self):
        return self.title