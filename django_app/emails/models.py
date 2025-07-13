from django.db import models
from django.utils import timezone


class ScheduledEmail(models.Model):
    """Model to store scheduled emails"""
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Email details
    topic = models.CharField(max_length=200, help_text="Email topic/subject")
    to_email = models.EmailField(help_text="Recipient email address")
    from_email = models.EmailField(help_text="Sender email address")
    app_password = models.CharField(max_length=100, help_text="Gmail app password")
    
    # Document and attachments
    doc_text = models.TextField(blank=True, help_text="Document content for AI analysis")
    document_file = models.FileField(upload_to='documents/', blank=True, null=True)
    attachment_files = models.JSONField(default=list, help_text="List of attachment file paths")
    
    # Scheduling
    scheduled_time = models.DateTimeField(help_text="When to send the email")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    sent_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, help_text="Error message if sending failed")
    
    # Generated content
    generated_subject = models.CharField(max_length=200, blank=True)
    generated_body = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Scheduled Email"
        verbose_name_plural = "Scheduled Emails"
    
    def __str__(self):
        return f"{self.topic} to {self.to_email} - {self.status}"
    
    @property
    def is_scheduled(self):
        return self.status == 'scheduled'
    
    @property
    def is_sent(self):
        return self.status == 'sent'
    
    @property
    def is_failed(self):
        return self.status == 'failed'
    
    @property
    def is_cancelled(self):
        return self.status == 'cancelled'
    
    def mark_as_sent(self):
        """Mark email as sent"""
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save(update_fields=['status', 'sent_at'])
    
    def mark_as_failed(self, error_message):
        """Mark email as failed"""
        self.status = 'failed'
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message'])
    
    def mark_as_cancelled(self):
        """Mark email as cancelled"""
        self.status = 'cancelled'
        self.save(update_fields=['status'])


class EmailAttachment(models.Model):
    """Model to store email attachments"""
    
    scheduled_email = models.ForeignKey(ScheduledEmail, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    original_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Email Attachment"
        verbose_name_plural = "Email Attachments"
    
    def __str__(self):
        return f"{self.original_name} for {self.scheduled_email.topic}"
