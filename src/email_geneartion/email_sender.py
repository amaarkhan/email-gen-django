import yagmail

def send_email(subject, body, to_email, from_email, app_password, attachments=None):
    try:
        yag = yagmail.SMTP(from_email, app_password)
        yag.send(to=to_email, subject=subject, contents=body, attachments=attachments)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
