from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import ScheduledEmail


class EmailForm(forms.ModelForm):
    """Form for creating and scheduling emails"""
    
    # Additional fields not in the model
    document = forms.FileField(
        required=False,
        label="Upload Document for Content (Optional)",
        help_text="This document will be analyzed by AI to generate email content. Supported formats: .txt, .pdf, .docx",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.txt,.pdf,.docx'
        })
    )
    
    attachments = forms.FileField(
        required=False,
        label="Upload Attachments (Optional)",
        help_text="These files will be attached to the email",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )
    
    send_now = forms.ChoiceField(
        choices=[('now', 'Send Now'), ('schedule', 'Schedule for Later')],
        initial='now',
        label="Send Option",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'onchange': 'toggleScheduleTime()'
        })
    )
    
    class Meta:
        model = ScheduledEmail
        fields = ['topic', 'to_email', 'from_email', 'app_password', 'scheduled_time']
        widgets = {
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What is this email about?'
            }),
            'to_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'recipient@example.com'
            }),
            'from_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@gmail.com'
            }),
            'app_password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '16-character app password'
            }),
            'scheduled_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'topic': 'Email Topic',
            'to_email': 'Recipient Email',
            'from_email': 'Your Gmail Address',
            'app_password': 'Gmail App Password',
            'scheduled_time': 'Schedule Send Time',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make scheduled_time optional initially
        self.fields['scheduled_time'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        send_now = cleaned_data.get('send_now')
        scheduled_time = cleaned_data.get('scheduled_time')
        
        if send_now == 'schedule':
            if not scheduled_time:
                raise ValidationError('Please select a send time for scheduled emails.')
            
            if scheduled_time <= timezone.now():
                raise ValidationError('Send time must be in the future.')
        
        return cleaned_data
    
    def clean_document(self):
        """Validate uploaded document"""
        document = self.cleaned_data.get('document')
        if document:
            allowed_extensions = ['.txt', '.pdf', '.docx']
            file_extension = '.' + document.name.split('.')[-1].lower()
            
            if file_extension not in allowed_extensions:
                raise ValidationError(f'Only {", ".join(allowed_extensions)} files are allowed for documents.')
            
            # Check file size (16MB limit)
            if document.size > 16 * 1024 * 1024:
                raise ValidationError('Document file size must be less than 16MB.')
        
        return document
