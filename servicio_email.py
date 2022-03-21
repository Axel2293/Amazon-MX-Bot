
#----------SMTP PROTOCOL----------------------#
import smtplib

def sendemail(message, em):
    # Use GMAIL account
    email="YOUR-EMAIL"
    password="YOUR-EMAIL-PASSWORD"
    send_to_email= em
    server=smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, send_to_email, message)
    print('EMAIL ENVIADO')
    server.quit()