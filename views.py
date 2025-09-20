from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Job, Application


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_Name")
        last_name = request.POST.get("last_Name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        choice = request.POST.get("role")

        if choice not in ['Employee', 'Employer']:
            messages.error(request, "Please select a valid role")
            return redirect('/register/')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('/register/')

        user = CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            choice=choice
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('/login/')

    return render(request, 'register.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        selected_role = request.POST.get("role")

        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Invalid username")
            return redirect('/login/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid password")
            return redirect('/login/')
        else:
            if user.choice != selected_role:
                messages.error(request, f"Incorrect role selected. You are registered as a {user.choice}.")
                return redirect('/login/')

            login(request, user)

            if user.choice == 'Employer':
                return redirect('/employer/')
            elif user.choice == 'Employee':
                return redirect('/employee/')
            else:
                return redirect('/login/')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login_page')


@login_required
def employee_view(request):
    jobs = Job.objects.all()
    return render(request, 'employee.html', {'jobs': jobs})



@login_required
def employer_view(request):
    jobs = Job.objects.all().prefetch_related("applications")
    return render(request, "employer.html", {"jobs": jobs})



@login_required
def create_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        requirments = request.POST.get('requirments')
        salary = request.POST.get('salary')
        deadline = request.POST.get('deadline')

        Job.objects.create(
            employer=request.user,  # Link job to employer
            title=title,
            description=description,
            requirments=requirments,
            salary=salary,
            deadline=deadline,
        )
        return redirect('/employer/')
    return render(request, 'create_job.html')



@login_required
def home_page(request):
    return render(request, "home.html")
# views.py
@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == "POST":
        cover_letter = request.POST.get("cover_letter")
        cv = request.FILES.get("cv")

        # Prevent duplicate applications
        if Application.objects.filter(job=job, employee=request.user).exists():
            messages.error(request, "You already applied for this job.")
            return redirect('/employee/')

        Application.objects.create(
            job=job,
            employee=request.user,
            cover_letter=cover_letter,
            cv=cv
        )
        messages.success(request, "Application submitted successfully!")
        return redirect('/employee/')

    return render(request, "apply_job.html", {"job": job})



def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = job.applications.all()  # all applications for this job
    return render(request, "view_applicants.html", {"job": job, "applications": applications})
