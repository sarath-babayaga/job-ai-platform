import os
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_application_email(
    candidate_name,
    job_title,
    company,
    location,
    match_score
):

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    subject = "Job Application Submitted"

    body = f"""
Job Application Submitted

Candidate : {candidate_name}

Role      : {job_title}

Company   : {company}

Location  : {location}

Match Score : {match_score}%

Applied Successfully
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender,
            password
        )

        server.send_message(msg)