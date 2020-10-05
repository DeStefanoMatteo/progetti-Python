# INVIARE EMAIL DA PYTHON

# Per impostare email:
import create_pdf
import datetime
import os.path
import pickle
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def config_email(receiver_email, pdf_file):
    port = 465  # For SSL
    sender_email = "..."
    password = "..."
    if receiver_email is None:
        receiver_email = "..."

    with open('report_statistics.pickle', 'rb') as f:
        w_stats = pickle.load(f)

    subject = f'Weight Report - {w_stats["date"]}'
    body = f'''Subject: Matteo De Stefano
    Date: {w_stats["date"]}

    Last weight: {w_stats['last_weight']} kg

    Median weight: {round(w_stats['median'], 1)} kg
    Max weight: {w_stats['max']} kg
    Min weight: {w_stats['min']} kg
    '''

    # Create a multipart message and set headers
    message = MIMEMultipart()  #  MIMEMultipart("alternative") for html body
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open PDF file in binary mode
    with open(f'reports/{pdf_file}', "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {pdf_file}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def main():
    pdf_file = f'weight_report_{datetime.date.today().strftime("%Y%m%d")}.pdf'
    if not os.path.isfile(f'reports/{pdf_file}'):
        # Create pdf report
        create_pdf.main()
        print(f'{pdf_file} created.')

    # Create and send email
    receiver_email = "..."
    config_email(receiver_email, pdf_file)
    print(f'E-mail sent to {receiver_email}.')


if __name__ == '__main__':
    main()
