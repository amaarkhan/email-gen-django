# Django Tests for Email App
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import ScheduledEmail, EmailAttachment


class ScheduledEmailModelTest(TestCase):
    """Test cases for ScheduledEmail model"""
    
    def setUp(self):
        self.email_data = {
            'topic': 'Test Email',
            'to_email': 'test@example.com',
            'from_email': 'sender@gmail.com',
            'app_password': 'testpassword123',
            'scheduled_time': timezone.now() + timedelta(hours=1),
            'doc_text': 'Test document content'
        }
    
    def test_create_scheduled_email(self):
        """Test creating a scheduled email"""
        email = ScheduledEmail.objects.create(**self.email_data)
        self.assertEqual(email.status, 'scheduled')
        self.assertTrue(email.is_scheduled)
        self.assertFalse(email.is_sent)
    
    def test_mark_as_sent(self):
        """Test marking email as sent"""
        email = ScheduledEmail.objects.create(**self.email_data)
        email.mark_as_sent()
        self.assertTrue(email.is_sent)
        self.assertIsNotNone(email.sent_at)
    
    def test_mark_as_failed(self):
        """Test marking email as failed"""
        email = ScheduledEmail.objects.create(**self.email_data)
        error_msg = "Test error"
        email.mark_as_failed(error_msg)
        self.assertTrue(email.is_failed)
        self.assertEqual(email.error_message, error_msg)
    
    def test_mark_as_cancelled(self):
        """Test marking email as cancelled"""
        email = ScheduledEmail.objects.create(**self.email_data)
        email.mark_as_cancelled()
        self.assertTrue(email.is_cancelled)


class EmailViewsTest(TestCase):
    """Test cases for email views"""
    
    def setUp(self):
        self.client = Client()
    
    def test_index_view(self):
        """Test the main index view"""
        response = self.client.get(reverse('emails:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI Email Generator')
        self.assertContains(response, 'Django')
    
    def test_scheduled_emails_view(self):
        """Test the scheduled emails view"""
        response = self.client.get(reverse('emails:scheduled_emails'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Scheduled Emails')
    
    def test_debug_scheduler_view(self):
        """Test the debug scheduler view"""
        response = self.client.get(reverse('emails:debug_scheduler'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_send_email_post_invalid(self):
        """Test sending email with invalid data"""
        response = self.client.post(reverse('emails:send_email'), {
            'topic': '',  # Empty topic should fail validation
            'send_now': 'now'
        })
        # Should return to form with errors
        self.assertEqual(response.status_code, 200)


class EmailFormTest(TestCase):
    """Test cases for EmailForm"""
    
    def test_form_valid_send_now(self):
        """Test form validation for send now"""
        from .forms import EmailForm
        
        form_data = {
            'topic': 'Test Email',
            'to_email': 'test@example.com',
            'from_email': 'sender@gmail.com',
            'app_password': 'testpassword123',
            'send_now': 'now'
        }
        form = EmailForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_schedule_no_time(self):
        """Test form validation for schedule without time"""
        from .forms import EmailForm
        
        form_data = {
            'topic': 'Test Email',
            'to_email': 'test@example.com',
            'from_email': 'sender@gmail.com',
            'app_password': 'testpassword123',
            'send_now': 'schedule'
            # Missing scheduled_time
        }
        form = EmailForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Please select a send time', str(form.errors))
