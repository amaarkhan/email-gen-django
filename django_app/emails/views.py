import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from werkzeug.utils import secure_filename

from .models import ScheduledEmail, EmailAttachment
from .forms import EmailForm

# Add the src directory to Python path for importing CrewAI modules
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent.parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

try:
    from email_geneartion.crew import EmailGeneartion
    from email_geneartion.doc_reader import read_document
    from email_geneartion.email_sender import send_email as send_email_smtp
except ImportError as e:
    print(f"Warning: Could not import CrewAI modules: {e}")
    # Create dummy functions for development
    class EmailGeneartion:
        def crew(self):
            class DummyCrew:
                def kickoff(self, inputs):
                    # Create a dummy generated email file
                    with open("generated_email.txt", "w") as f:
                        f.write(f"Subject: Email about {inputs['topic']}\n\nThis is a generated email about {inputs['topic']}.")
                        f.write(f"Subject: {inputs['topic']}\n\nThis is a test email generated for: {inputs['topic']}")
            return DummyCrew()
    
    def read_document(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return "Could not read document"
    
    def send_email_smtp(subject, body, to_email, from_email, app_password, attachments=None):
        print(f"Would send email: {subject} to {to_email}")

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()


class IndexView(TemplateView):
    """Main page with email form"""
    template_name = 'emails/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmailForm()
        return context


class ScheduledEmailsView(ListView):
    """View to list all scheduled emails"""
    model = ScheduledEmail
    template_name = 'emails/scheduled_emails.html'
    context_object_name = 'emails'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add scheduler status
        context['scheduler_status'] = {
            'running': scheduler.running,
            'total_jobs': len(scheduler.get_jobs()),
            'current_time': timezone.now().isoformat(),
        }
        return context


def generate_email_content(topic, doc_text):
    """Generate email content using CrewAI"""
    try:
        inputs = {
            "topic": topic,
            "doc_text": doc_text,
            "current_year": str(datetime.now().year)
        }
        
        print(f"🤖 Generating email for topic: {topic}")
        EmailGeneartion().crew().kickoff(inputs=inputs)
        
        # Read generated email
        with open("generated_email.txt", "r", encoding="utf-8") as f:
            email_content = f.read().strip()
        
        # Extract subject and body
        lines = email_content.splitlines()
        subject = "Generated Email"
        body_lines = []
        
        for i, line in enumerate(lines):
            if line.lower().startswith("subject:"):
                subject = line.replace("Subject:", "").replace("subject:", "").strip()
                start_idx = i + 1
                while start_idx < len(lines) and not lines[start_idx].strip():
                    start_idx += 1
                body_lines = lines[start_idx:]
                break
        else:
            body_lines = lines
            
        body = "\n".join(body_lines).strip()
        
        return subject, body
        
    except Exception as e:
        print(f"❌ Error generating email: {e}")
        return f"Error generating email: {str(e)}", "Please try again or contact support."


def send_scheduled_email(email_id):
    """Function to send scheduled emails"""
    try:
        scheduled_email = ScheduledEmail.objects.get(id=email_id)
        print(f"📧 Sending scheduled email to: {scheduled_email.to_email}")
        
        # Generate email content
        subject, body = generate_email_content(scheduled_email.topic, scheduled_email.doc_text)
        
        # Get attachment files
        attachment_paths = []
        for attachment in scheduled_email.attachments.all():
            if attachment.file:
                attachment_paths.append(attachment.file.path)
        
        # Send email
        send_email_smtp(
            subject=subject,
            body=body,
            to_email=scheduled_email.to_email,
            from_email=scheduled_email.from_email,
            app_password=scheduled_email.app_password,
            attachments=attachment_paths
        )
        
        # Update email status
        scheduled_email.generated_subject = subject
        scheduled_email.generated_body = body
        scheduled_email.mark_as_sent()
        
        print(f"✅ Scheduled email sent successfully to {scheduled_email.to_email}")
                
    except ScheduledEmail.DoesNotExist:
        print(f"❌ Scheduled email with ID {email_id} not found")
    except Exception as e:
        print(f"❌ Error sending scheduled email: {e}")
        try:
            scheduled_email = ScheduledEmail.objects.get(id=email_id)
            scheduled_email.mark_as_failed(str(e))
        except:
            pass


def send_email(request):
    """Handle email sending/scheduling"""
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                print(f"📝 Processing email request...")
                
                # Handle document upload for content
                doc_text = ""
                if form.cleaned_data.get('document'):
                    doc_file = form.cleaned_data['document']
                    doc_path = default_storage.save(f'documents/{doc_file.name}', doc_file)
                    full_doc_path = os.path.join(settings.MEDIA_ROOT, doc_path)
                    doc_text = read_document(full_doc_path)
                    print(f"📄 Document uploaded: {doc_file.name}")
                
                # Create scheduled email instance
                scheduled_email = form.save(commit=False)
                scheduled_email.doc_text = doc_text
                
                if form.cleaned_data['send_now'] == 'now':
                    # Send immediately
                    scheduled_email.scheduled_time = timezone.now()
                    scheduled_email.save()
                    
                    print("📧 Sending email immediately...")
                    subject, body = generate_email_content(scheduled_email.topic, doc_text)
                    
                    # Handle attachments
                    attachment_paths = []
                    if form.cleaned_data.get('attachments'):
                        attach_file = form.cleaned_data['attachments']
                        attach_path = default_storage.save(f'attachments/{attach_file.name}', attach_file)
                        full_attach_path = os.path.join(settings.MEDIA_ROOT, attach_path)
                        attachment_paths.append(full_attach_path)
                        
                        # Create attachment record
                        EmailAttachment.objects.create(
                            scheduled_email=scheduled_email,
                            file=attach_path,
                            original_name=attach_file.name
                        )
                    
                    # Add files from Attach_folders
                    attach_folder = settings.ATTACH_FOLDER
                    if os.path.exists(attach_folder):
                        for file_name in os.listdir(attach_folder):
                            file_path = os.path.join(attach_folder, file_name)
                            if os.path.isfile(file_path):
                                attachment_paths.append(file_path)
                    
                    send_email_smtp(
                        subject=subject,
                        body=body,
                        to_email=scheduled_email.to_email,
                        from_email=scheduled_email.from_email,
                        app_password=scheduled_email.app_password,
                        attachments=attachment_paths
                    )
                    
                    scheduled_email.generated_subject = subject
                    scheduled_email.generated_body = body
                    scheduled_email.mark_as_sent()
                    
                    messages.success(request, '✅ Email sent successfully!')
                    
                else:
                    # Schedule email
                    scheduled_email.save()
                    
                    # Handle attachments
                    if form.cleaned_data.get('attachments'):
                        attach_file = form.cleaned_data['attachments']
                        attach_path = default_storage.save(f'attachments/{attach_file.name}', attach_file)
                        
                        EmailAttachment.objects.create(
                            scheduled_email=scheduled_email,
                            file=attach_path,
                            original_name=attach_file.name
                        )
                    
                    print(f"⏰ Scheduling email for: {scheduled_email.scheduled_time}")
                    
                    # Add to scheduler
                    job = scheduler.add_job(
                        func=send_scheduled_email,
                        trigger=DateTrigger(run_date=scheduled_email.scheduled_time),
                        args=[scheduled_email.id],
                        id=str(scheduled_email.id)
                    )
                    
                    messages.success(request, f'⏰ Email scheduled for {scheduled_email.scheduled_time.strftime("%Y-%m-%d %H:%M")}!')
                
                return redirect('emails:index')
                
            except Exception as e:
                print(f"❌ Error processing email: {e}")
                messages.error(request, f'❌ Error: {str(e)}')
        
        else:
            # Form validation failed
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'❌ {field}: {error}')
    
    else:
        form = EmailForm()
    
    return render(request, 'emails/index.html', {'form': form})


def cancel_email(request, pk):
    """Cancel a scheduled email"""
    scheduled_email = get_object_or_404(ScheduledEmail, pk=pk)
    
    if scheduled_email.is_scheduled:
        # Remove from scheduler
        try:
            scheduler.remove_job(str(pk))
        except:
            pass  # Job might have already been executed or removed
        
        # Update status
        scheduled_email.mark_as_cancelled()
        
        messages.success(request, f'✅ Email scheduled for {scheduled_email.to_email} has been cancelled.')
    else:
        messages.error(request, '❌ Email cannot be cancelled.')
    
    return redirect('emails:scheduled_emails')


def debug_scheduler(request):
    """Debug endpoint to check scheduler status"""
    jobs = scheduler.get_jobs()
    scheduled_emails = ScheduledEmail.objects.filter(status='scheduled')
    
    return JsonResponse({
        'running': scheduler.running,
        'jobs_count': len(jobs),
        'jobs': [{'id': job.id, 'next_run': str(job.next_run_time)} for job in jobs],
        'scheduled_emails_count': scheduled_emails.count(),
        'scheduled_emails': [
            {
                'id': email.id,
                'topic': email.topic,
                'to_email': email.to_email,
                'scheduled_time': email.scheduled_time.isoformat(),
                'status': email.status,
            }
            for email in scheduled_emails
        ]
    })


def test_scheduler(request):
    """Test endpoint to verify scheduler is working"""
    test_time = timezone.now() + timedelta(seconds=10)
    
    def test_function():
        print(f"🎯 [{timezone.now()}] Test scheduler job executed successfully!")
    
    job = scheduler.add_job(
        func=test_function,
        trigger=DateTrigger(run_date=test_time),
        id=f"test_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
    )
    
    return JsonResponse({
        'message': f'Test job scheduled for {test_time}',
        'job_id': job.id
    })
