from django.urls import path
from . import views

urlpatterns = [
    path('student_registration/',views.student_register,name='student_registration'),
    path('student_login/',views.student_login,name='student_login')
]