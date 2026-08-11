from django.contrib import admin
from .models import (
    JobCategory,
    Company,
    Job,
    Candidate,
    JobApplication,
    Recruiter,
    ContactMessage
)

admin.site.register(JobCategory)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Candidate)
admin.site.register(JobApplication)
admin.site.register(Recruiter)
admin.site.register(ContactMessage)