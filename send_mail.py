import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail SMTP server configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587  # Port for TLS
smtp_user = "developer@skylink.net.in"  # Your Gmail address
smtp_password = "dkoqlcsxagoywdeh"  # Your Gmail app password

# Email content
sender_email = "developer@skylink.net.in"
receiver_email = "developer@skylink.net.in"
subject = "Test Email from Python"
body = "This is a test email sent using Gmail SMTP in Python."

# Create the email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# Send the email
try:
    # Set up the SMTP server and start the TLS encryption
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection

    # Log in to the server
    server.login(smtp_user, smtp_password)

    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")

except Exception as e:
    print(f"Error: {e}")

finally:
    server.quit()  # Close the connection to the SMTP server
