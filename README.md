# Python_mail_class
Python class for sending emails in a simple way.
Supports sending emails to multiple adresses at once.

Examaple of sending email:

my_string = 'Send email with Python'
MailObject = Mail('smtp.mail.com', 587)
MailObject.set_sender('my_mail@mail.com', 'password')
MailObject.set_destination(['mail1@y.com','mail2@y.com'])
MailObject.send_email('Subject',message='Message',payload=['1.txt','2.doc','3.jpg'], virtual_payload={'name.txt':my_string})

