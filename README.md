# 🚀 Django AI Email Generator & Scheduler

A powerful Django web application that combines AI intelligence with email automation. Generate professional, context-aware emails using CrewAI and Gemini AI, schedule them for future delivery, and manage everything through a beautiful, responsive web interface.

## ✨ What Makes This Special?

🤖 **AI-Powered Writing**: Let Gemini AI craft professional emails based on your documents and requirements  
📅 **Smart Scheduling**: Schedule emails for any future date and time with automatic delivery  
📁 **Document Intelligence**: Upload PDFs, Word docs, or text files for AI content analysis  
📎 **Easy Attachments**: Drag-and-drop file uploads with support for multiple attachments  
📧 **Gmail Ready**: Seamless integration with Gmail using secure App Passwords  
📊 **Management Dashboard**: View, edit, and cancel scheduled emails with real-time status  
🎨 **Beautiful UI**: Modern, responsive design powered by Bootstrap 5  
🔐 **Admin Panel**: Full Django admin interface for advanced management  

## 🎯 Perfect For

- **Business Professionals** scheduling follow-up emails
- **Job Seekers** sending personalized applications
- **Content Creators** automating newsletter delivery
- **Students** submitting assignments on time
- **Anyone** who wants AI-powered email assistance

## 🚀 Quick Start (5 Minutes Setup)

### What You'll Need
- Python 3.8+ installed on your computer
- A Gmail account (free)
- Google Gemini API key (free tier available)

### Step 1: Get Your Project
```bash
git clone https://github.com/amaarkhan/email-gen-django.git
cd email-gen-django
```

### Step 2: Install Everything
```bash
# Install Python dependencies
pip install django==4.2.23 crewai yagmail PyPDF2 python-docx APScheduler python-dotenv

# Set up the database
python manage.py migrate

# Create an admin user (optional but recommended)
python manage.py createsuperuser
```

### Step 3: Configure Your Settings
Create a `.env` file in the project root:
```env
# Your Gemini AI API Key (get from https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key_here

# Email settings (you can also enter these in the web form)
DEFAULT_EMAIL=your.email@gmail.com
DEFAULT_PASSWORD=your_gmail_app_password
```

### Step 4: Start the Application
```bash
python manage.py runserver
```

### Step 5: Open and Enjoy!
Open your browser and go to: **http://127.0.0.1:8000**

## � How to Use

### 🎯 Send an Email Right Now

1. **Go to the main page** (http://127.0.0.1:8000)
2. **Fill out the form**:
   - **Email Topic**: What's your email about? (e.g., "Job Application", "Meeting Request")
   - **Upload Document**: Choose a file to analyze (PDF, Word, or text)
   - **Add Attachments**: Upload any files you want to attach
   - **Recipient Email**: Who are you sending to?
   - **Your Gmail**: Your Gmail address
   - **App Password**: Your Gmail App Password (see setup guide below)
3. **Select "Send Now"**
4. **Click "Generate & Send Email"**
5. **Done!** AI will read your document, write a professional email, and send it

### ⏰ Schedule for Later

1. **Fill out the same form** as above
2. **Select "Schedule for Later"**
3. **Pick your date and time** using the date picker
4. **Click "Generate & Send Email"**
5. **Relax!** Your email will be sent automatically at the scheduled time

### 📊 Manage Your Scheduled Emails

- **View all scheduled emails**: Go to http://127.0.0.1:8000/scheduled/
- **Cancel emails**: Click the "Cancel" button next to any email
- **Check status**: See if emails are pending, sent, or failed
- **Admin panel**: Go to http://127.0.0.1:8000/admin/ for advanced management

## 🔧 Setup Guides

### 🔑 Getting Your Gemini API Key (Free!)

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" → "Create API Key"
4. Copy the key and paste it in your `.env` file
5. **Free tier includes**: 15 requests per minute, 1 million tokens per minute

### 📧 Setting Up Gmail App Password

**Why do I need this?** Gmail requires App Passwords for third-party applications for security.

1. **Enable 2-Factor Authentication**:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Turn on 2-Step Verification if not already enabled

2. **Create App Password**:
   - In the same Security page, find "App passwords"
   - Select app: "Mail"
   - Copy the 16-character password (no spaces)
   - Use this password in the application, NOT your regular Gmail password

### 🗂️ Supported File Types

| Type | Extensions | What it's good for |
|------|------------|-------------------|
| **Text** | `.txt` | Simple documents, notes, requirements |
| **PDF** | `.pdf` | Resumes, reports, official documents |
| **Word** | `.docx` | Letters, proposals, formatted documents |

## 🎨 Project Structure

```
email-gen-django/
├── 📱 Django App
│   ├── emails/                 # Main Django app
│   │   ├── models.py          # Database models
│   │   ├── views.py           # Web pages and logic
│   │   ├── forms.py           # Web forms
│   │   └── templates/         # HTML templates
│   ├── manage.py              # Django management
│   └── settings.py            # Configuration
├── 🤖 AI Components
│   ├── src/email_geneartion/
│   │   ├── crew.py            # AI crew setup
│   │   ├── doc_reader.py      # Document reading
│   │   └── config/            # AI agent settings
├── 📁 File Storage
│   ├── uploads/               # User uploaded files
│   ├── Attach_folders/        # Default attachments
│   └── media/                 # Django media files
└── 📊 Database
    └── db.sqlite3             # SQLite database
```

## 🛠️ Advanced Features

### Admin Panel
Access the powerful Django admin at `/admin/` to:
- View all emails in the database
- Manually create/edit scheduled emails
- Monitor system performance
- Manage users and permissions

### API Integration
The system uses:
- **CrewAI**: For AI agent coordination
- **Gemini AI**: For natural language processing
- **APScheduler**: For background email scheduling
- **Django ORM**: For database management

### Customization
Want to modify the AI behavior?
- Edit `src/email_geneartion/config/agents.yaml` for agent personalities
- Edit `src/email_geneartion/config/tasks.yaml` for task descriptions
- Modify templates in `emails/templates/` for UI changes

## ❓ Troubleshooting & FAQ

### 🚨 Common Issues & Quick Fixes

**Problem**: "ModuleNotFoundError" when starting
```bash
# Solution: Install missing dependencies
pip install django==4.2.23 crewai yagmail PyPDF2 python-docx APScheduler python-dotenv
```

**Problem**: "CSRF verification failed"
- **Solution**: Make sure cookies are enabled in your browser
- Clear browser cache and try again

**Problem**: "Gmail authentication error"
- **Solution**: 
  - Use App Password, NOT your regular Gmail password
  - Make sure 2-Factor Authentication is enabled
  - Check for typos in your email/password

**Problem**: "Template syntax error"
- **Solution**: This is a known issue we're working on. The app still functions for email generation.

**Problem**: "Permission denied" on file uploads
- **Solution**: Make sure the `uploads/` and `media/` folders exist and are writable

### 💡 Pro Tips

1. **Test with yourself first**: Send your first email to your own address to see how it works
2. **Use descriptive topics**: Better topics = better AI-generated emails
3. **Upload relevant documents**: The AI writes better emails when it has context
4. **Check spam folders**: First-time emails might go to spam
5. **Schedule ahead**: Give yourself buffer time for important emails

### 🔍 Advanced Troubleshooting

**Check if Django is working**:
```bash
python manage.py check
```

**Reset the database** (if needed):
```bash
python manage.py flush
python manage.py migrate
```

**View detailed error logs**:
- Check the terminal where you ran `python manage.py runserver`
- Look for detailed error messages

**Test email sending manually**:
```python
# In Django shell: python manage.py shell
import yagmail
yag = yagmail.SMTP('your.email@gmail.com', 'your_app_password')
yag.send('test@example.com', 'Test Subject', 'Test Body')
```

## 🤝 Contributing & Support

### Found a Bug?
1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with:
   - Steps to reproduce
   - Error messages
   - Your Python/Django version

### Want to Contribute?
1. Fork the repository
2. Create a feature branch: `git checkout -b amazing-feature`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Need Help?
- 📧 **Email**: Create an issue on GitHub
- 📖 **Documentation**: This README covers most use cases
- 💬 **Community**: Check GitHub discussions

## 📜 License & Credits

### Open Source License
This project is licensed under the MIT License - feel free to use, modify, and distribute.

### Built With Love Using:
- 🐍 **Django** - The web framework for perfectionists with deadlines
- 🤖 **CrewAI** - Multi-agent AI framework
- 🧠 **Google Gemini** - Advanced language model
- 🎨 **Bootstrap 5** - Beautiful, responsive UI
- 📧 **Yagmail** - Simple email sending
- ⏰ **APScheduler** - Background task scheduling

### Special Thanks
- Google for providing free Gemini AI API
- The Django community for excellent documentation
- CrewAI team for making AI agents accessible
- Bootstrap team for making beautiful UIs easy

---

## 🎉 You're All Set!

**Congratulations!** You now have a powerful AI email assistant running on your computer. Start by sending yourself a test email, then explore all the features.

**Remember**: The AI gets better with more context, so don't hesitate to upload documents and write detailed topics for the best results.

**Happy emailing!** 🚀📧✨
