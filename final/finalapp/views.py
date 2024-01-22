
from django.shortcuts import redirect, render
from .form import *
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import CustomUser
from django.http import JsonResponse
from django.db.models import Q


# Create your views here.


def home(request):
    job_user = request.user
    user = CustomUser.objects.get(username=job_user.username)
    #
    if user.role == "jober":
        if request.method == 'POST':
            # Get the search parameters from the form
            search_date = request.POST.get('formattedDate')

        # Perform the search based on the provided parameters
            # hiring = Hiring.objects.filter(event_date=search_date)
            hiring = Hiring.objects.filter(
                Q(event_date=search_date) & ~Q(
                    selected_user__contains=[job_user.username])
            )
        # hiring = Hiring.objects.exclude(
        #     selected_user__contains=[job_user.username]).filter(total_members__gte=len(selected_user))
        else:
            hiring = Hiring.objects.exclude(
                selected_user__contains=[job_user.username])
        context = {"hiring": hiring, }
        return render(request, "finalapp/index.html", context)
    elif user.role == "hirer":
        return redirect("hiringform")
    else:
        return HttpResponse("Invalid role.")


def job(request):
    job_user = request.user
    jb = Hiring.objects.filter(selected_user__contains=[job_user.username])
    return render(request, "finalapp/job.html", {"jb": jb})


def profile(request):
    return render(request, "finalapp/profile.html")


def hirerprofile(request):
    return render(request, "finalapp/hirerprofile.html")


def update_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        ploc1 = request.POST.get('ploc1')
        ploc2 = request.POST.get('ploc2')
        # Get the current user
        user = CustomUser.objects.get(username=request.user.username)

        # Update user's information
        user.name = name
        user.email = email
        user.phone_number = phone_number
        user.ploc1 = ploc1
        user.ploc2 = ploc2
        user.save()

        data = {
            'success': True,
            'message': 'Profile updated successfully!',
            'user': {
                'name': user.name,
                'email': user.email,
                'phone_number': user.phone_number,
                'ploc1': user.ploc1,
                'ploc2': user.ploc2,

            }
        }

        return JsonResponse(data)

    data = {'success': False, 'message': 'Invalid request'}
    return JsonResponse(data)


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(
            request, "logged out successfully")
        return redirect('login')


def login_page(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pswd = request.POST.get('password')
        user = authenticate(request, username=name, password=pswd)
        if user is not None:
            login(request, user)
            messages.success(
                request, "logged in successfully ")
            return redirect('/')
        else:
            messages.error(
                request, "Invalid username or password")
            return redirect('/login')
    return render(request, "finalapp/login.html")


@login_required(login_url='login')  # Redirect to login page if not logged in
def first_page(request):
    # Redirect to home page if already logged in
    return redirect('home')

# @login_required
# def dashboard(request):
#     return redirect('home')


# def login_page(request):
#     if request.method == 'POST':
#         name = request.POST.get('username')
#         pswd = request.POST.get('password')
#         try:
#             user = User.objects.get(username=name)
#             if user.check_password(pswd):
#                 login(request, user)
#                 messages.success(
#                     request, "logged in successfully ")
#                 return redirect('dashboard')
#             else:
#                 messages.error(
#                     request, "Invalid username or password")
#                 return redirect('/login')
#         except User.DoesNotExist:
#             messages.error(
#                 request, "Invalid username or password")
#             return redirect('/login')
#     return render(request, "app_job/login.html")


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, "Registraion Success You Can Login Now! ")
            return redirect('/login')
    return render(request, "finalapp/register.html", {'form': form})


def hired(request):
    hired = Hiring.objects.filter(created_by__username=request.user.username)
    context = {
        "hired": hired,
    }
    return render(request, "finalapp/hired.html", context)


def hiringform(request):
    if request.method == 'POST':
        form = HiringForm(request.POST)
        if form.is_valid():
            # Add the created_by field before saving the form
            hiring = form.save(commit=False)
            hiring.vacancy = form.cleaned_data['total_members']
            hiring.created_by = request.user
            hiring.save()
            return redirect('home')
    else:
        form = HiringForm()
    return render(request, 'finalapp/hiringform.html', {'form': form})


def add_to_job(request, job_id):
    job_user = request.user
    selected = Hiring.objects.get(id=job_id)
    selected.selected_user += [job_user.username]
    selected.save()
    return redirect('home')


def decline(request, job_id_remove):
    job_user = request.user
    declined = Hiring.objects.get(id=job_id_remove)
    declined.selected_user.remove(job_user.username)
    declined.save()
    return redirect('job')


def delete_hired(request, del_hired_id):
    delhir = Hiring.objects.get(id=del_hired_id)
    delhir.delete()
    return redirect('hired')


def completed_view(request):
    # Handle the form submission
    if request.method == 'POST':
        # Assuming you have a hidden input field in your form to store the hiring_id
        hiring_id = request.POST.get('hiring_id')
        # Assuming 'attendees' is the name attribute of your checkboxes
        selected_users = request.POST.getlist('attendees')

        # Retrieve the hiring instance
        hiring_instance = Hiring.objects.get(pk=hiring_id)
        # Fetch details of selected users from CustomUser model
        selected_users_details = CustomUser.objects.filter(
            username__in=selected_users)

        # Create a list of dictionaries containing username and phone_number
        selected_users_data = [
            {'user': user.username, 'phone': user.phone_number}
            for user in selected_users_details
        ]

        # Create a completed instance and save it
        completed_instance = completed_jobs(
            manager_name=hiring_instance.manager_name,
            event_date=hiring_instance.event_date,
            start_time=hiring_instance.start_time,
            end_time=hiring_instance.end_time,
            event_location=hiring_instance.event_location,
            attend_user=selected_users_data,
        )
        completed_instance.save()
        hiring_instance.delete()

        messages.success(request, 'Attendance submitted successfully!')
        # Replace 'your_redirect_url' with the URL where you want to redirect after form submission
        return redirect('hired')


def signout(request):
    deluser = CustomUser.objects.get(username=request.user.username)
    if (request.user.role == "jober"):
        delhire = Hiring.objects.all()
        for i in delhire:
            i.selected_user.remove(request.user.username)
            i.save()
    elif (request.user.role == "Hirer"):
        pass
    deluser.delete()

    return redirect('register')
