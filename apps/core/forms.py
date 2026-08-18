import os
import re
from django import forms
from django.core.exceptions import ValidationError

from .models import ContactMessage, JobApplication


class ContactForm(forms.ModelForm):
    # Honeypot field for bot defense (must stay empty, a11y-safe)
    website_source_check = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"tabindex": "-1", "autocomplete": "off", "aria-hidden": "true"}),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "company", "email", "phone", "inquiry_type", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Your Full Name", "class": "form-input", "required": "required"}
            ),
            "company": forms.TextInput(
                attrs={"placeholder": "Company / Organization (Optional)", "class": "form-input"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "corporate@domain.com", "class": "form-input", "required": "required"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "+20 1X XXXX XXXX", "class": "form-input"}
            ),
            "inquiry_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Provide details regarding your project scope, tender requirements, or inquiry...",
                    "class": "form-textarea",
                    "rows": 5,
                    "required": "required",
                }
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if phone:
            # Normalize multiple spaces and ensure clean format
            phone = re.sub(r"\s+", " ", phone)
        return phone

    def clean(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.get("website_source_check")
        if honeypot:
            # Bot filled hidden field
            raise ValidationError("Spam submission detected.")
        return cleaned_data


class JobApplicationForm(forms.ModelForm):
    # Honeypot field for bot defense (a11y-safe)
    website_source_check = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"tabindex": "-1", "autocomplete": "off", "aria-hidden": "true"}),
    )

    class Meta:
        model = JobApplication
        fields = ["full_name", "email", "phone", "cover_note", "resume"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your Full Name", "class": "form-input", "required": "required"}),
            "email": forms.EmailInput(attrs={"placeholder": "email@address.com", "class": "form-input", "required": "required"}),
            "phone": forms.TextInput(attrs={"placeholder": "+20 1X XXXX XXXX", "class": "form-input", "required": "required"}),
            "cover_note": forms.Textarea(attrs={"placeholder": "Brief introduction or cover note...", "class": "form-textarea", "rows": 3}),
            "resume": forms.FileInput(attrs={"class": "form-file-input", "accept": ".pdf,.doc,.docx"}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if phone:
            phone = re.sub(r"\s+", " ", phone)
        return phone

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")
        if resume:
            # 10 MB maximum limit
            max_size_mb = 10
            if resume.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Resume file size cannot exceed {max_size_mb}MB.")

            # Extension validation
            ext = os.path.splitext(resume.name)[1].lower()
            valid_extensions = [".pdf", ".doc", ".docx"]
            if ext not in valid_extensions:
                raise ValidationError("Unsupported file format. Please upload a PDF, DOC, or DOCX document.")
        return resume

    def clean(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.get("website_source_check")
        if honeypot:
            raise ValidationError("Spam submission detected.")
        return cleaned_data
