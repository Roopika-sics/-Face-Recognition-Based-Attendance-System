from django.contrib import admin
from .models import User, Faculty, Face, Attendance

admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(Face)
admin.site.register(Attendance)
