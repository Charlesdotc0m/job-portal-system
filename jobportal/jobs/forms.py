from django import forms
from django.contrib.auth.models import User
from .models import Candidate, Job


class CandidateForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
    )

    class Meta:
        model = Candidate

        fields = [
            'candidate_name',
            'email',
            'phone',
            'resume',
            'skills',
        ]

        widgets = {
            'candidate_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),

            'resume': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Example: Python, Django, React, SQL'
            }),
        }

    def save(self, commit=True):

        candidate = super().save(commit=False)

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = User.objects.create_user(
            username=username,
            email=candidate.email,
            password=password
        )

        candidate.user = user

        if commit:
            candidate.save()

        return candidate


# =========================================
# JOB FORM
# =========================================

class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            'job_title',
            'job_description',
            'salary',
            'location',
            'company',
            'category',
        ]

        widgets = {

            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title'
            }),

            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe the job responsibilities, requirements, and qualifications'
            }),

            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 500000',
                'step': '0.01'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: Chennai, Tamil Nadu'
            }),

            'company': forms.Select(attrs={
                'class': 'form-select'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }