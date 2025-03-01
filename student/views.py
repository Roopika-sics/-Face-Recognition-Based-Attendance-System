from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from .models import Student
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout


def student_register(request):
    if request.method == "POST":
        name = request.POST['name']
        student_id = request.POST['student-id']
        email = request.POST['email']
        department = request.POST['department']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        photo = request.FILES.get('photo') 

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('student_registration')

        if Student.objects.filter(student_id=student_id).exists() or Student.objects.filter(email=email).exists():
            messages.error(request, "Student ID or Email already exists!")
            return redirect('student_registration')
        

        student = Student(
            student_name=name,
            student_id=student_id,
            email=email,
            department=department,
            password=make_password(password),  
            photo=photo
        )
        print(f'student: {student}')
        student.save()

        messages.success(request, "Registration successful!")
        return redirect('student_login')

    return render(request,'student/registration.html')

def student_login(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        if not student_id or not password:
            messages.error(request, "Both fields are required!")
            return render(request, 'student/login.html')

        user = authenticate(request, username=student_id, password=password)

        print(f'USER: {user}')

        if user is not None:
            login(request, user)
            return redirect('student/student_profile')
        else:
            messages.error(request, "Invalid Credentials!")

    return render(request, 'student/login.html')


def student_logout(request):
    logout(request)
    return redirect("student/login.html")

def student_profile(request, student_id):
    student = Student.objects.filter(student_id=student_id).first()
    return render(request, 'student/student_profile.html', {'student': student})


def student_landing_page(request):
    return render(request,'student/student_landing.html')
