import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviarCorreo(correo_electronico, asunto, mensaje, txt):
    me = "notificaciones@ives.edu.mx" #"Correo de quien envia el mensaje" 
    you = correo_electronico #"Correo de a quien se le envia el mensaje" 

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = asunto
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = txt
    html = mensaje

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('notificaciones@ives.edu.mx', 'q7RtZv$RY92dp$NB')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()