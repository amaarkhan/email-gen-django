# AI Email Scheduler & Generator

A comprehensive web-based email generation and scheduling system using CrewAI framework with a beautiful Flask frontend. Generate and schedule professional emails with AI assistance, document analysis, and attachment support.

## 🌟 Features

- **🌐 Web Interface**: Beautiful, responsive web frontend for easy email management
- **⏰ Email Scheduling**: Schedule emails for future delivery with date/time picker
- **📄 Document Analysis**: Upload and analyze `.txt`, `.pdf`, and `.docx` files for content
- **🤖 AI-Powered Generation**: Uses Gemini AI to craft professional, context-aware emails
- **📎 File Attachments**: Upload multiple attachments or use files from `Attach_folders`
- **📧 Gmail Integration**: Secure sending via Gmail SMTP with App Password
- **📊 Scheduling Dashboard**: View, manage, and cancel scheduled emails
- **🔄 Real-time Status**: Track email status (scheduled, sent, failed, cancelled)
- **📱 Mobile Friendly**: Responsive design works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Gmail account with App Password enabled
- Google Gemini API key

### Installation

1. **Clone and navigate to the project**:
   ```bash
   git clone <your-repo-url>
   cd crewai-email-generation/email_geneartion
   ```

2. **Install dependencies**:
   ```bash
   uv install
   # OR
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   MODEL=gemini/gemini-1.5-flash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Start the web application**:
   ```bash
   python run_flask_app.py
   # OR
   python -m src.email_geneartion.app
   ```

5. **Open your browser**:
   Navigate to `http://localhost:5000`

## 🖥️ Web Interface Usage

### 📧 Send Email Immediately

1. **Fill in the form**:
   - Enter email topic (e.g., "Job Application", "Meeting Request")
   - Upload a document for AI content analysis (optional)
   - Add file attachments (optional)
   - Enter recipient and your Gmail details
   - Enter your Gmail App Password

2. **Select "Send Now"** and click "Process Email"

3. **AI will**:
   - Analyze your document
   - Generate professional email content
   - Send immediately to recipient

### ⏰ Schedule Email for Later

1. **Fill in the form** (same as above)

2. **Select "Schedule for Later"**

3. **Pick date and time** using the datetime picker

4. **Click "Process Email"**

5. **Email will be automatically sent** at the scheduled time

### 📊 Manage Scheduled Emails

- **View scheduled emails**: Navigate to `/scheduled_emails`
- **Cancel emails**: Click cancel button next to any scheduled email
- **Check status**: See if emails are scheduled, sent, failed, or cancelled
- **Debug scheduler**: Visit `/debug/scheduler` for technical details

## Project Structure

```
email_geneartion/
├── src/
│   └── email_geneartion/
│       ├── main.py              # Main application entry point
│       ├── crew.py              # CrewAI crew configuration
│       ├── doc_reader.py        # Document reading utilities
│       ├── email_sender.py      # Email sending functionality
│       └── config/
│           ├── agents.yaml      # AI agent configurations
│           └── tasks.yaml       # Task definitions
├── docs/                        # Place your documents here
├── Attach_folders/             # Place files to attach here
├── pyproject.toml              # Project dependencies
└── .env                        # Environment variables
```

## Usage

1. **Run the application**:
   ```bash
   crewai run
   ```

2. **Follow the prompts**:
   - Enter the topic/subject of your email
   - Provide the path to your document (e.g., `docs/req.txt`)
   - Enter recipient's email address
   - Enter your Gmail address
   - Enter your Gmail App Password

3. **File attachments**:
   - Place any files you want to attach in the `Attach_folders` directory
   - The system will automatically include all files from this folder

## Supported Document Types

- **Text files** (`.txt`)
- **PDF files** (`.pdf`) - requires PyPDF2
- **Word documents** (`.docx`) - requires python-docx

## Dependencies

- `crewai[tools]` - AI crew framework
- `yagmail` - Email sending
- `PyPDF2` - PDF reading
- `python-docx` - Word document reading

## Configuration

### Agents (config/agents.yaml)
- **doc_extractor**: Analyzes and extracts key information from documents
- **email_writer**: Generates professional emails from extracted information

### Tasks (config/tasks.yaml)
- **extract_doc_task**: Extracts relevant information from the provided document
- **generate_email_task**: Creates a complete email with subject and body

## Example Usage

```bash
# Start the application
crewai run

# Example inputs:
# Topic: "Application for Frontend Developer Position"
# Document: "docs/job_application.txt"
# Recipient: "hr@company.com"
# Your Gmail: "your.email@gmail.com"
# App Password: "your16charpassword"
```

## Output

The system will:
1. Analyze your document
2. Generate a professional email with proper subject and body
3. Send the email with any attachments from `Attach_folders`
4. Save the generated email to `generated_email.txt`

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: 
   ```bash
   uv install  # Reinstall dependencies
   ```

2. **API Key Invalid**:
   - Check your `.env` file
   - Verify your Gemini API key is correct
   - Ensure no extra spaces in the API key

3. **Gmail Authentication Error**:
   - Ensure 2-factor authentication is enabled
   - Use App Password, not regular password
   - Check Gmail security settings

4. **File Not Found**:
   - Verify document path is correct
   - Use relative paths from the project root
   - Check file permissions

### API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Copy the key to your `.env` file
4. Ensure the key has proper permissions

### Gmail App Password Setup

1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Go to App Passwords
4. Generate password for "Mail"
5. Use this 16-character password in the application

## Development

To modify the email generation logic:
- Edit `config/agents.yaml` to change agent behavior
- Edit `config/tasks.yaml` to modify task descriptions
- Modify `crew.py` to change the workflow

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify your API keys and passwords
3. Ensure all dependencies are installed
4. Check file paths and permissions
