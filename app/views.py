from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from student.models import Student,LeaveRequest
from django.http import HttpResponseForbidden, JsonResponse
# from django.contrib.auth.hashers import make_password
from .models import Faculty,Event
import json
from datetime import datetime


#Admin 
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("dashboard")
        else:
                messages.error(request, "Need admin credentials to access this page.")
                
    return render(request, "login.html")

def admin_logout(request):
    logout(request)
    return redirect("admin_login")


def student_list(request):
     students = Student.objects.filter(is_staff=False, is_active=True)
     return render(request, 'student_list.html', {'students': students})



def view_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect('student_list')

    return render(request, 'view_student.html', {'student': student})



def delete_student(request, student_id):
    if request.method == "POST":
        student = get_object_or_404(Student, id=student_id)
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect("student_list")

    return HttpResponseForbidden("Invalid request method.")


#FACULTY
def faculty_list(request):
    return render(request,'faculty_list.html')




#Faculty_Registration
def create_faculty(request):
    if request.method == "POST":
        faculty_id = request.POST.get("faculty_id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if not faculty_id or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("create_faculty")
        
        try:
            Faculty.objects.get(faculty_id=faculty_id)
            messages.error(request, "Faculty ID already exists.")
            return redirect("create_faculty")
        except Faculty.DoesNotExist:
            Faculty.objects.create_faculty(faculty_id=faculty_id, email=email, password=password)
            messages.success(request, "Registration successful!")
            return redirect("faculty_login")
    
    return render(request, "create_faculty.html")


def faculty_login(request):
    if request.method == "POST":
        faculty_id = request.POST.get("faculty_id")
        password = request.POST.get("password")
        
        if not faculty_id or not password:
            messages.error(request, "All fields are required.")
            return redirect("faculty_login")
        
        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id)
            if faculty.check_password(password):
                messages.success(request, "Login successful!")
                return redirect("faculty_dashboard")
            else:
                messages.error(request, "Invalid password.")
        except Faculty.DoesNotExist:
            messages.error(request, "Faculty ID not found.")
    
    return render(request, "faculty_login.html")


def faculty_logout(request):
    logout(request)
    return redirect("faculty_login")


def faculty_dashboard(request):

    total_students = Student.objects.filter(is_superuser=False).count()
    leaves = LeaveRequest.objects.filter(status='Pending').order_by('-applied_on')

    user = request.user
    
    context = {
        'total_students': total_students,
        'user': user,
        'leaves': leaves

    }
    return render(request,'faculty_dashboard.html',context)


def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = 'Approved'
    leave.save()
    messages.success(request, 'Leave request approved!')
    return redirect('faculty_dashboard')

def decline_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = 'Declined'
    leave.save()
    messages.error(request, 'Leave request declined!')
    return redirect('faculty_dashboard')


@login_required(login_url='/')
@never_cache
def dashboard(request):
    response = render(request, "dashboard.html")
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response






def faculty_calendar(request):
    return render(request,'faculty_calendar.html')



def get_events(request):
    events = Event.objects.all()
    
    event_list = []
    for event in events:
        print(f"Event: {event.title}, Start: {event.start}, Color: {event.color}")
        
        event_list.append({
            "id": event.id,
            "title": event.title,
            "start": event.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "description": event.description,
            "color": event.color,
            "backgroundColor": event.color,
            "borderColor": event.color,
        })
    
    return JsonResponse(event_list, safe=False)




def add_event(request):
    if request.method == "POST":
        title = request.POST.get("title")
        start = request.POST.get("start_date")
        color = request.POST.get("color","#337BFF")
        description = request.POST.get("description")


        start = datetime.strptime(start, "%Y-%m-%dT%H:%M")

        # Save event
        Event.objects.create(
            title=title,
            start=start,
            color = color,
            description=description
        )
        return redirect("faculty_calendar")

    return render(request, "add_event.html")


def delete_event(request, event_id):
    if request.method == "DELETE":
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return JsonResponse({"message": "Event deleted!"})
    return JsonResponse({"error": "Invalid request"}, status=400)