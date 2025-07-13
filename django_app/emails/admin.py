from django.contrib import admin
from .models import ScheduledEmail, EmailAttachment


@admin.register(ScheduledEmail)
class ScheduledEmailAdmin(admin.ModelAdmin):
    """Admin interface for ScheduledEmail model"""
    
    list_display = [
        'topic', 'to_email', 'from_email', 'status', 
        'scheduled_time', 'created_at', 'sent_at'
    ]
    list_filter = ['status', 'created_at', 'scheduled_time']
    search_fields = ['topic', 'to_email', 'from_email']
    readonly_fields = ['created_at', 'updated_at', 'sent_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Email Details', {
            'fields': ('topic', 'to_email', 'from_email', 'app_password')
        }),
        ('Content', {
            'fields': ('doc_text', 'document_file', 'generated_subject', 'generated_body')
        }),
        ('Scheduling', {
            'fields': ('scheduled_time', 'status')
        }),
        ('Status', {
            'fields': ('sent_at', 'error_message', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Only allow deletion of cancelled or failed emails
        if obj and obj.status in ['cancelled', 'failed']:
            return True
        return False


@admin.register(EmailAttachment)
class EmailAttachmentAdmin(admin.ModelAdmin):
    """Admin interface for EmailAttachment model"""
    
    list_display = ['original_name', 'scheduled_email', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['original_name', 'scheduled_email__topic']
    readonly_fields = ['uploaded_at']
