from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        'jobs/',
        views.jobs,
        name='jobs'
    ),

    path(
        'companies/',
        views.companies,
        name='companies'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),

    path(
        'categories/',
        views.categories,
        name='categories'
    ),

    path(
        'candidate/register/',
        views.candidate_register,
        name='candidate_register'
    ),

    path(
        'login/',
        views.user_login,
        name='user_login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='user_logout'
    ),

    path(
        'candidate/portal/',
        views.candidate_portal,
        name='candidate_portal'
    ),

    path(
        'job/<int:job_id>/',
        views.job_detail,
        name='job_detail'
    ),

    path(
        'job/<int:job_id>/apply/',
        views.apply_job,
        name='apply_job'
    ),

    path(
        'candidate/applications/',
        views.my_applications,
        name='my_applications'
    ),

    path(
        'recruiter/portal/',
        views.recruiter_portal,
        name='recruiter_portal'
    ),

    path(
        'recruiter/application/<int:application_id>/update/',
        views.update_application_status,
        name='update_application_status'
    ),
    path(
        'recruiter/post-job/',
        views.recruiter_post_job,
        name='recruiter_post_job'
    ),
    path(
        'recruiter/login/',
        views.recruiter_login,
        name='recruiter_login'
    ),
]
