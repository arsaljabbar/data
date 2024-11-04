import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import zipfile
import datetime
import argparse

# Get current date to add to the email subject
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Zip the folder
def zip_directory(folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname)

# Create and send the email
def send_email(sender_email, receiver_email, email_password, smtp_server, smtp_port, zip_file_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f'Daily Zip File {current_date}'

    # Attach the zip file
    with open(zip_file_path, 'rb') as attachment:
        mime_base = MIMEBase('application', 'octet-stream')
        mime_base.set_payload(attachment.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_file_path)}')
        msg.attach(mime_base)

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Main function to zip and send the file
if __name__ == '__main__':
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description="Zip a directory and send it via email.")
    parser.add_argument('--sender_email', required=True, help='Sender email address')
    parser.add_argument('--receiver_email', required=True, help='Receiver email address')
    parser.add_argument('--email_password', required=True, help='Password for sender email')
    parser.add_argument('--smtp_server', default='smtp.example.com', help='SMTP server address')
    parser.add_argument('--smtp_port', type=int, default=587, help='SMTP server port')
    parser.add_argument('--directory_to_zip', required=True, help='Directory path to zip')
    parser.add_argument('--zip_file_name', default='test.zip', help='Name for the output zip file')

    args = parser.parse_args()

    # Zip the directory
    zip_directory(args.directory_to_zip, args.zip_file_name)

    # Send the email
    send_email(args.sender_email, args.receiver_email, args.email_password, args.smtp_server, args.smtp_port, args.zip_file_name)
