from django.shortcuts import render

def student_register(request):
    return render(request,'student/registration.html')

def student_login(request):
    return render(request,'student/login.html')