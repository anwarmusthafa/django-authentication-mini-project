from django.shortcuts import render,redirect
from . models import Students
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.db import IntegrityError


# Create your views here.
@never_cache
def home(request):
    if 'name' in request.session:
        return render(request, 'home.html')
    return redirect('login')
@never_cache
def login(request):
    if 'name' in request.session:
        return redirect('home')
    error_message = None
    if request.POST:
        name =  request.POST.get('name')
        password =  request.POST.get('password')
        try:
            user = Students.objects.get(name=name.lower(), password=password)
        except Students.DoesNotExist:
            user = None
        if user is not None:
            request.session['name'] = name
            return redirect('home')
        else:
            error_message = "This user is not available"
    return render(request,'login.html',{'error_message':error_message} )
def signup(request):
    error_messages = {
        'password_error': None,
        'email_error': None,
        'name_error': None,
        'phone_error': None,
    }
    registration_successfull = None

    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password_1 = request.POST.get('password1')
        password_2 = request.POST.get('password2')

        if password_1 != password_2 or len(password_1) < 6:
            if password_1 != password_2:
                error_messages['password_error'] = "Password 1 and Password 2 do not match."
            else:
                error_messages['password_error'] = "Password length should be minimum 6 "
        elif len(phone) != 10 or not phone.isdigit() or len(name) < 4 or not name.replace(" ","").isalpha():
            if len(name) < 4 or not name.replace(" ", "").isalpha():
                error_messages['name_error'] = "Name should have a minimum of 4 characters and only contain alphabets."
            if len(phone) != 10 or not phone.isdigit():
                error_messages['phone_error'] = "Phone Number should have exactly 10 digits."

        else:
            try:
                my_user = Students.objects.create(name=name.lower(), email=email, phone=phone, password=password_1)
                my_user.save()
                registration_successfull = "Your Registration is Successfull"
                return render(request, 'signup.html', {'registration_successfull' : registration_successfull})
            except IntegrityError as e:
                if 'duplicate key value violates unique constraint "students_students_email_key"' in str(e):
                    error_messages['email_error'] = "An account with this email already exists."
                else:
                    error_messages['error_message'] = "An error occurred during signup. Please try again."

    return render(request, 'signup.html', error_messages)
def logout(request):
    if 'name' in request.session:
        request.session.flush()
    return redirect('login')
    
