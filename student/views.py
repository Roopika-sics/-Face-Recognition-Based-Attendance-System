from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Student,PasswordReset,LeaveRequest
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime,date
from app.models import Event
import re



def validate_password(password):

    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character.")
    
    return errors


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
        
        password_errors = validate_password(password)
        if password_errors:
            for error in password_errors:
                messages.error(request, error)
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
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful!") 
            profile_url = reverse('student_profile', kwargs={'student_id': user.student_id})
            return redirect(profile_url)
        else:
            messages.error(request, "Invalid Credentials!")

    return render(request, 'student/login.html')


def student_logout(request):
    logout(request)
    return redirect("student/student_landing_page")

def student_profile(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'student/student_profile.html', {'student': student})



def student_landing_page(request):
    return render(request,'student/student_landing.html')


def forget_password(request):
    
    if request.method =="POST":
        email = request.POST.get('email')

        try:
            user = Student.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        

            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )

            email_message.fail_silently = False
            email_message.send()

            return HttpResponseRedirect(reverse("password-reset-sent", kwargs={"reset_id": new_password_reset.reset_id}))
        
        except Student.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request,'student/forget_password.html')


def password_reset_sent(request,reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'student/password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')


def reset_password(request,reset_id):
    
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')
            
            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('student_login')
            
            else:
                return redirect('reset-password',reset_id=reset_id)

    
    
    except PasswordReset.DoesNotExist:
        
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'student/reset_password.html',{'reset_id': reset_id})




def apply_leave(request):
    student = get_object_or_404(Student, email=request.user.email)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        # Validate input dates
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Please select a valid date.")
            return redirect('apply_leave')

        # Prevent selecting past dates
        if start_date_obj < date.today():
            messages.error(request, "Start date cannot be in the past.")
            return redirect('apply_leave')

        if end_date_obj < start_date_obj:
            messages.error(request, "End date cannot be before the start date.")
            return redirect('apply_leave')

        # Calculate total leave days
        total_days = (end_date_obj - start_date_obj).days + 1

        # Check if leave already applied for the same dates
        existing_leave = LeaveRequest.objects.filter(
            student=student,
            start_date__lte=end_date_obj,
            end_date__gte=start_date_obj
        ).exists()

        if existing_leave:
            messages.error(request, "You have already applied for leave on the selected dates.")
            return redirect('apply_leave')

        # Check leave balance
        if student.leave_balance < total_days:
            messages.error(request, f"You only have {student.leave_balance} leave days remaining.")
            return redirect('apply_leave')

        # Deduct leave balance and save leave request
        student.leave_balance -= total_days
        student.save()

        LeaveRequest.objects.create(
            student=student,
            reason=reason,
            start_date=start_date_obj,
            end_date=end_date_obj,
            status='Pending'
        )

        messages.success(request, f"Leave request submitted successfully. {total_days} day(s) leave deducted from your balance.")

        return redirect(reverse('student_profile', kwargs={'student_id': student.student_id}))

    return render(request, 'student/apply_leave.html', {'student': student})


def leave_status(request):
    student = Student.objects.get(email=request.user.email)
    leaves = LeaveRequest.objects.filter(student=student).order_by('-applied_on')
    return render(request, 'student/leave_status.html', {'leaves': leaves})


def calendar(request):
    student = Student.objects.all()
    print(student)
    return render(request,'student/calendar.html',{'student': student})



def get_events(request):
    events = Event.objects.all()
    event_list = [
        {
            "id": event.id,
            "title": event.title,
            "start": event.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "description": event.description,
            "color": event.color if event.color else "#3b82f6",
        }
        for event in events
    ]
    return JsonResponse(event_list, safe=False)



def edit_profile(request):
    student = Student.objects.get(email=request.user.email)

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('name')
        department = request.POST.get('department')
        email = request.POST.get('email')

        student.student_id = student_id
        student.student_name = student_name
        student.department = department
        student.email = email
        student.save()

        messages.success(request, "Profile updated successfully!")
        profile_url = reverse('student_profile', kwargs={'student_id': student.student_id})
        return redirect(profile_url)

    return render(request, 'student/edit_profile.html', {'user': student})


def about(request):
    return render(request,'student/about_page.html')


def contact(request):
    return render(request,'student/contact.html')