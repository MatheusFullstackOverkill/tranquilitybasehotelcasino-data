import json
import base64
import smtplib, ssl
import functions_framework
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = "o.goncalves.matheus@gmail.com"
password = "wajviaprsbgutymo"

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
   # Print out the data from Pub/Sub, to prove that it worked
   data = json.loads(base64.b64decode(cloud_event.data["message"]["data"]))
   print(data)

   context = ssl.create_default_context()
   with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(email, password)

      msg = MIMEMultipart('alternative')
      msg['Subject'] = "Come Stay With Us! - Tranquility Base Hotel & Casino"
      msg['From'] = email
      msg['To'] = data['email']
      # Plain-text version of content
      plain_text = """\
         Hi there,
         This message is sent from Python Geeks.
         Visit us here https://pythongeeks.net
         Have a good day!
      """
      # html version of content
      email_file_content = open('user_email.html', 'r')
      html_content = email_file_content.read()
      email_file_content.close()

      text_part = MIMEText(plain_text, 'plain')
      html_part = MIMEText(html_content, 'html')

      msg.attach(text_part)
      msg.attach(html_part)

      response = server.send_message(msg)
      print(response) 

      msg = MIMEMultipart('alternative')
      msg['Subject'] = "New Contact - Tranquility Base Hotel & Casino"
      msg['From'] = email
      msg['To'] = email

      plain_text = """\
         Hi there,
         This message is sent from Python Geeks.
         Visit us here https://pythongeeks.net
         Have a good day!
      """

      email_file_content = open('admin_email.html', 'r')
      html_content = email_file_content.read()
      email_file_content.close()
      html_content = html_content.replace('email</p>', data['email']+'</p>')
      html_content = html_content.replace('fullname</p>', data['fullname']+'</p>')
      html_content = html_content.replace('message</p>', data['message']+'</p>')


      text_part = MIMEText(plain_text, 'plain')
      html_part = MIMEText(html_content, 'html')

      msg.attach(text_part)
      msg.attach(html_part)

      response = server.send_message(msg)
      print(response)
