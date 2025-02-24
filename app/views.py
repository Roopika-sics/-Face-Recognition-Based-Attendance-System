from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


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

@login_required(login_url='/')
@never_cache
def dashboard(request):
    response = render(request, "dashboard.html")
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response