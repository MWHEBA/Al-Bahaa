from django import forms

from .models import ContactMessage, JobApplication


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]


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

