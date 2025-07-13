from email_sender import send_email

# Read generated email from CrewAI output
with open("generated_email.txt", "r", encoding="utf-8") as f:
    email_content = f.read()

# You can extract subject from first line (if your email content has one)
lines = email_content.strip().splitlines()
subject = lines[0].replace("Subject: ", "") if lines[0].lower().startswith("subject") else "Email from CrewAI"
body = "\n".join(lines)

# YOUR credentials
your_email = "i220759@nu.edu.pk"
app_password = "oari swol posd ltmw"
receiver_email = "amaarkhan25@gmail.com"

# Send
send_email(subject, body, receiver_email, your_email, app_password)
