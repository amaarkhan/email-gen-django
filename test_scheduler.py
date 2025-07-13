#!/usr/bin/env python
"""
Test script to verify email scheduling functionality
"""
import requests
import json
from datetime import datetime, timedelta

def test_scheduler():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Email Scheduler Functionality")
    print("=" * 50)
    
    # 1. Test scheduler status
    print("📊 Checking scheduler status...")
    try:
        response = requests.get(f"{base_url}/debug/scheduler")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Scheduler running: {data['running']}")
            print(f"📋 Total jobs: {data['jobs_count']}")
            print(f"📧 Scheduled emails: {data['scheduled_emails_count']}")
        else:
            print(f"❌ Failed to get scheduler status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking scheduler: {e}")
    
    print()
    
    # 2. Test scheduler with a quick test job
    print("⏰ Testing scheduler with 10-second test job...")
    try:
        response = requests.get(f"{base_url}/test_scheduler")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Test job scheduled: {data['message']}")
            print(f"⏱️  Check console in: 10 seconds")
        else:
            print(f"❌ Failed to schedule test job: {response.status_code}")
    except Exception as e:
        print(f"❌ Error scheduling test: {e}")
    
    print()
    
    # 3. Check scheduled emails
    print("📋 Checking scheduled emails...")
    try:
        response = requests.get(f"{base_url}/scheduled_emails")
        if response.status_code == 200:
            print("✅ Scheduled emails page accessible")
        else:
            print(f"❌ Failed to access scheduled emails: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing scheduled emails: {e}")
    
    print()
    print("🔗 URLs to test manually:")
    print(f"   - Main App: {base_url}")
    print(f"   - Scheduled Emails: {base_url}/scheduled_emails")
    print(f"   - Scheduler Debug: {base_url}/debug/scheduler")
    print(f"   - Test Scheduler: {base_url}/test_scheduler")

if __name__ == "__main__":
    test_scheduler()

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import time

def test_function(message, test_id):
    """Test function to be scheduled"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"🎯 [{current_time}] Scheduled task executed: {message} (ID: {test_id})")

def test_scheduler():
    """Test the scheduler functionality"""
    print("🚀 Testing APScheduler...")
    
    # Initialize scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()
    print("📅 Scheduler started")
    
    # Schedule a test job for 10 seconds from now
    test_time = datetime.now() + timedelta(seconds=10)
    print(f"⏰ Scheduling test for: {test_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    job = scheduler.add_job(
        func=test_function,
        trigger=DateTrigger(run_date=test_time),
        args=["Test message", "test123"],
        id="test_job"
    )
    
    print(f"✅ Job scheduled with ID: {job.id}")
    print("⏳ Waiting for execution... (15 seconds)")
    
    # Wait for 15 seconds to see if the job executes
    time.sleep(15)
    
    # Shutdown scheduler
    scheduler.shutdown()
    print("🛑 Scheduler shutdown")

if __name__ == "__main__":
    test_scheduler()
