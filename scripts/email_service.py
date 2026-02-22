#!/usr/bin/env python3
"""Gmail SMTP Email Service for OpenClaw - with attachment support"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 載入環境變數 (手動讀取)
env_vars = {}
env_path = "/home/node/.openclaw/workspace/.env"
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=', 1)
                env_vars[k] = v

# Gmail SMTP 配置
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = env_vars.get("GMAIL_USER", "smlhtliu@gmail.com")
APP_PASSWORD = env_vars.get("GMAIL_APP_PASSWORD", "")

def send_email(to_email, subject, body, attachment_path=None):
    """發送 Email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 添加附件
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    import sys
    
    to_email = sys.argv[1] if len(sys.argv) > 1 else None
    subject = sys.argv[2] if len(sys.argv) > 2 else "No Subject"
    body = sys.argv[3] if len(sys.argv) > 3 else ""
    attachment = sys.argv[4] if len(sys.argv) > 4 else None
    
    if not to_email:
        print("Usage: python3 email_service.py <to_email> <subject> <body> [attachment_path]")
        sys.exit(1)
    
    success, message = send_email(to_email, subject, body, attachment)
    print(message)
    sys.exit(0 if success else 1)
