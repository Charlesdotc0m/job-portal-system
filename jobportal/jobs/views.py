from django.shortcuts import render, redirect

from .models import (
    Job,
    Company,
    JobCategory,
    Candidate,
    JobApplication,
    Recruiter,
    ContactMessage
)

from .forms import CandidateForm, JobForm

from django.contrib.auth import authenticate, login, logout


# =========================
# HOME
# =========================

def home(request):

    featured_jobs = Job.objects.all().order_by('-id')[:3]

    latest_jobs = Job.objects.all().order_by('-id')[:6]

    companies = Company.objects.all().order_by('-id')[:6]

    categories = JobCategory.objects.all().order_by('-id')[:8]

    return render(request, 'home.html', {
        'featured_jobs': featured_jobs,
        'latest_jobs': latest_jobs,
        'companies': companies,
        'categories': categories,
    })


# =========================
# ABOUT
# =========================

def about(request):

    return render(request, 'about.html')


# =========================
# JOBS + SEARCH + CATEGORY
# =========================

def jobs(request):

    search_query = request.GET.get('search', '').strip()

    location_query = request.GET.get('location', '').strip()

    category_id = request.GET.get('category', '').strip()

    all_jobs = Job.objects.all().order_by('-id')

    # Search by job title
    if search_query:

        all_jobs = all_jobs.filter(
            job_title__icontains=search_query
        )

    # Search by location
    if location_query:

        all_jobs = all_jobs.filter(
            location__icontains=location_query
        )

    # Filter by category
    if category_id:

        all_jobs = all_jobs.filter(
            category_id=category_id
        )

    # Get all categories for dropdown
    all_categories = JobCategory.objects.all().order_by(
        'category_name'
    )

    return render(request, 'jobs.html', {

        'jobs': all_jobs,

        'search_query': search_query,

        'location_query': location_query,

        'category_id': category_id,

        'categories': all_categories,

    })


# =========================
# COMPANIES
# =========================

def companies(request):

    companies = Company.objects.all().order_by('-id')

    return render(request, 'companies.html', {

        'companies': companies

    })


# =========================
# CONTACT
# =========================

def contact(request):

    if request.method == 'POST':

        name = request.POST.get('name')

        email = request.POST.get('email')

        subject = request.POST.get('subject')

        message = request.POST.get('message')

        ContactMessage.objects.create(

            name=name,

            email=email,

            subject=subject,

            message=message

        )

        return render(request, 'contact.html', {

            'success': 'Your message has been sent successfully!'

        })

    return render(request, 'contact.html')


# =========================
# JOB CATEGORIES
# =========================

def categories(request):

    categories = JobCategory.objects.all().order_by('-id')

    return render(request, 'categories.html', {

        'categories': categories

    })


# =========================
# CANDIDATE REGISTRATION
# =========================

def candidate_register(request):

    if request.method == 'POST':

        form = CandidateForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('user_login')

    else:

        form = CandidateForm()

    return render(request, 'candidate_register.html', {

        'form': form

    })


# =========================
# USER LOGIN
# =========================

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('candidate_portal')

        else:

            return render(request, 'login.html', {

                'error': 'Invalid username or password.'

            })

    return render(request, 'login.html')


# =========================
# USER LOGOUT
# =========================

def user_logout(request):

    logout(request)

    return redirect('home')


# =========================
# CANDIDATE PORTAL
# =========================

def candidate_portal(request):

    if not request.user.is_authenticated:

        return redirect('user_login')

    try:

        candidate = Candidate.objects.get(
            user=request.user
        )

    except Candidate.DoesNotExist:

        candidate = None

    return render(request, 'candidate_portal.html', {

        'candidate': candidate

    })


# =========================
# JOB DETAIL
# =========================

def job_detail(request, job_id):

    job = Job.objects.get(
        id=job_id
    )

    return render(request, 'job_detail.html', {

        'job': job

    })


# =========================
# APPLY JOB
# =========================

def apply_job(request, job_id):

    if not request.user.is_authenticated:

        return redirect('user_login')

    try:

        candidate = Candidate.objects.get(
            user=request.user
        )

    except Candidate.DoesNotExist:

        return redirect('candidate_register')

    job = Job.objects.get(
        id=job_id
    )

    if request.method == 'POST':

        JobApplication.objects.create(

            candidate=candidate,

            job=job

        )

        return redirect('candidate_portal')

    return render(request, 'apply_job.html', {

        'job': job,

        'candidate': candidate

    })


# =========================
# MY APPLICATIONS
# =========================

def my_applications(request):

    if not request.user.is_authenticated:

        return redirect('user_login')

    try:

        candidate = Candidate.objects.get(
            user=request.user
        )

    except Candidate.DoesNotExist:

        return redirect('candidate_register')

    applications = JobApplication.objects.filter(

        candidate=candidate

    ).select_related(

        'job',

        'job__company',

        'job__category'

    ).order_by('-application_date')

    return render(request, 'my_applications.html', {

        'applications': applications

    })


# =========================
# RECRUITER PORTAL
# =========================

def recruiter_portal(request):

    if not request.user.is_authenticated:

        return redirect('user_login')

    try:

        recruiter = Recruiter.objects.get(
            email=request.user.email
        )

    except Recruiter.DoesNotExist:

        return render(request, 'recruiter_portal.html', {

            'recruiter': None,

            'applications': []

        })

    applications = JobApplication.objects.filter(

        job__company=recruiter.company

    ).select_related(

        'candidate',

        'job',

        'job__company'

    ).order_by('-application_date')

    return render(request, 'recruiter_portal.html', {

        'recruiter': recruiter,

        'applications': applications

    })


# =========================
# UPDATE APPLICATION STATUS
# =========================

def update_application_status(
    request,
    application_id
):

    if not request.user.is_authenticated:

        return redirect('user_login')

    try:

        recruiter = Recruiter.objects.get(
            email=request.user.email
        )

    except Recruiter.DoesNotExist:

        return redirect('user_login')

    application = JobApplication.objects.get(

        id=application_id,

        job__company=recruiter.company

    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        if new_status in dict(
            JobApplication.STATUS_CHOICES
        ):

            application.status = new_status

            application.save()

        return redirect('recruiter_portal')

    return render(request, 'update_status.html', {

        'application': application

    })


# =========================
# RECRUITER POST JOB
# =========================

def recruiter_post_job(request):

    if not request.user.is_authenticated:

        return redirect('user_login')

    try:

        recruiter = Recruiter.objects.get(
            email=request.user.email
        )

    except Recruiter.DoesNotExist:

        return redirect('recruiter_portal')

    if request.method == 'POST':

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            # Recruiter's company automatically selected
            job.company = recruiter.company

            job.save()

            return redirect('recruiter_portal')

    else:

        form = JobForm()

        # Recruiter can only post for their company
        form.fields['company'].initial = recruiter.company

    return render(request, 'recruiter_post_job.html', {

        'form': form,

        'recruiter': recruiter

    })


# =========================
# RECRUITER LOGIN
# =========================

def recruiter_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            try:

                Recruiter.objects.get(
                    email=user.email
                )

                login(request, user)

                return redirect('recruiter_portal')

            except Recruiter.DoesNotExist:

                return render(
                    request,
                    'recruiter_login.html',
                    {
                        'error':
                        'This account is not registered as a recruiter.'
                    }
                )

        else:

            return render(
                request,
                'recruiter_login.html',
                {
                    'error':
                    'Invalid username or password.'
                }
            )

    return render(
        request,
        'recruiter_login.html'
    )
