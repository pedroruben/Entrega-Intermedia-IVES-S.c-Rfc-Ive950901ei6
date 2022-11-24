import smtplib 
from email.message import EmailMessage 

def enviarCorreo(nombre):
    print(f'Hola {nombre}')

email_subject = "Asunto del correo" 
sender_email_address = "Correo de quien envia el mensaje" 
receiver_email_address = "Correo de a quien se le envia el mensaje" 
email_smtp = "smtp.gmail.com" #se queda así
email_password = "contraseña del correo que envia el mensaje" 

# Create an email message object 
message = EmailMessage() 

# Configure email headers 
message['Subject'] = email_subject 
message['From'] = sender_email_address 
message['To'] = receiver_email_address 

# Set email body text 
message.set_content("Hello from Python!") #mensaje
#:::::::::::::::::::::::::::::::::::::::::::::::::::::
# #Para enviar un mensaje de una plantilla html
# # Create an email message object
# message = EmailMessage()

# # Read file containing html
# with open('templates/mensaje.html', 'r') as file:
#    file_content = file.read()

# # Add message content as html type
# message.set_content(file_content, subtype='html')
#:::::::::::::::::::::::::::::::::::::::::::::::::::::
# Set smtp server and port 
server = smtplib.SMTP(email_smtp, '587') 

# Identify this client to the SMTP server 
server.ehlo() 

# Secure the SMTP connection 
server.starttls() 

# Login to email account 
server.login(sender_email_address, email_password) 

# Send email 
server.send_message(message) 

# Close connection to server 
server.quit()

#https://loopgk.com/2021/03/05/enviando-emails-con-python-guia-completa/