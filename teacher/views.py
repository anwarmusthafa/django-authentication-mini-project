from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from students.models import Students
from django.views.decorators.cache import never_cache

from .forms import StudentForm

 

# Create your views here.
@never_cache
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_home')
    error_message = None
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return redirect("admin_home")
        else:
            error_message = "Invalid Username and Password"
    return render(request,"admin_login.html",{"error_message":error_message})
@never_cache
@login_required(login_url="admin_login")
def admin_home(request):
    if request.user.is_authenticated:
        search_query = None
        if 'q' in request.GET:
            q = request.GET['q']
            search_query = True
            students = Students.objects.filter(name__icontains=q)
        else:
            students = Students.objects.all().order_by('name')
        return render(request, "admin_home.html", {'students': students, 'search_query': search_query})
    else:
        # Handle the case when the user is not authenticated, e.g., redirect to login page
        return redirect('admin_login')
@login_required(login_url='admin_login')
def add_student(request):
    # if request.user.is_authenticated:
        student_add = None
        if request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            student = Students.objects.create(name = name.lower(), email = email,phone = phone, password = password)
            student.save()
            student_add = "New student is succesfully added"
        return render(request, "add_student.html", {"student_add":student_add})
@login_required(login_url='admin_login')
def admin_logout(request):
        auth_logout(request)
        return redirect('admin_login')
@login_required(login_url='admin_login')
def edit_student(request, pk):
        instance_to_be_edit = get_object_or_404(Students, pk=pk)
        if request.method == 'POST':
            instance_to_be_edit.name = request.POST.get("name")
            instance_to_be_edit.email = request.POST.get("email")
            instance_to_be_edit.phone = request.POST.get("phone")
            instance_to_be_edit.password = request.POST.get("password")
            instance_to_be_edit.save()
            return redirect("admin_home")
        return render(request, 'edit_student.html', { 'instance_to_be_edit': instance_to_be_edit,'pk': pk})
@login_required(login_url='admin_login')
def delete_student(request,pk):
    # if request.user.is_authenticated:
        instance = Students.objects.get(pk=pk)
        instance.delete()
        students = Students.objects.all()
        return render(request,"admin_home.html", {'students':students})


    
