from django import forms

from .models import ContactMessage, JobApplication


class ContactForm(forms.ModelForm):
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


class JobApplicationForm(forms.ModelForm):
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

