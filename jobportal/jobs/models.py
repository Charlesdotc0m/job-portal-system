from django.db import models
from django.contrib.auth.models import User


class JobCategory(models.Model):
    category_name = models.CharField(max_length=100)
    category_description = models.TextField()

    def __str__(self):
        return self.category_name


class Company(models.Model):
    company_name = models.CharField(max_length=150)
    company_logo = models.ImageField(upload_to='company_logos/')
    company_location = models.CharField(max_length=150)
    company_description = models.TextField()

    def __str__(self):
        return self.company_name


class Job(models.Model):
    job_title = models.CharField(max_length=150)
    job_description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=150)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        JobCategory,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.job_title


class Candidate(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    candidate_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    skills = models.TextField()

    def __str__(self):
        return self.candidate_name


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    application_date = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    def __str__(self):
        return f"{self.candidate} - {self.job}"


class Recruiter(models.Model):
    recruiter_name = models.CharField(max_length=150)
    email = models.EmailField()

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.recruiter_name

class ContactMessage(models.Model):

    name = models.CharField(max_length=150)

    email = models.EmailField()

    subject = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"