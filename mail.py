# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename


class Mail(object):
    """
    Class for sending emails.
    Smtp server is set during initialization.
    Destination addresses are set by set_destination()
    Sender is set by set_sender()
    Emails are sent by send_email()
    """
    def __init__(self, smtp, port):
        """
        Init fucntion.
        smtp: str, smtp server name
        port: int, smtp server port number
        """
        self.smtp = smtp
        self.port = port
        self.sender = None
        self.password = None
        self.destination = None

    def set_smtp(self, smtp):
        """
        Sets smtp server name.
        :param smtp: str
        :return: None
        """
        self.smtp = smtp

    def set_port(self, port):
        """
        Sets smtp server port.
        :param port: int
        :return: None
        """
        self.port = port

    def get_smtp_server(self):
        """
        :return: list, smtp name - str, port number - int
        """
        return [self.smtp, self.port]

    def send_email(self, subject, message=None, payload=None, virtual_payload=None):
        """
        Sends email for each address in destination list.
        :param subject:str
        :param message:str
        :param payload:list of strings
        :param virtual_payload:dictionary filename:variable
        :return:None
        """
        assert(type(payload) == list or payload is None), 'Payload type should be list.'
        assert (type(virtual_payload) == dict or virtual_payload is None), 'Payload type should be dict.'
        assert(self.sender is not None and self.password is not None), 'Sender is not defined.'
        assert(self.destination is not None), 'Destination is not defined.'
        server = smtplib.SMTP(self.smtp, self.port)
        server.starttls()
        server.login(self.sender, self.password)
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['Subject'] = subject
        if payload is not None:
            for item in payload:
                with open(item, 'rb') as f:
                    part = MIMEApplication(f.read(), Name=basename(item))
                part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(item))
                msg.attach(part)
        if message is not None:
            text = MIMEText(message.decode('utf-8'), 'plain', 'utf-8')
            msg.attach(text)
        if virtual_payload is not None:
            i = 1
            for key in virtual_payload:
                part2 = MIMEApplication(virtual_payload[key], Name=key)
                part2['Content-Disposition'] = 'attachment; filename="{}"'.format(key)
                msg.attach(part2)
                i += 1
        for addr in self.destination:
            msg['To'] = addr
            server.sendmail(self.sender, addr, msg.as_string())
        server.quit()

    def set_sender(self, sender, password):
        """
        Sets sender email and password
        :param sender:str
        :param password:str
        :return:None
        """
        self.sender = sender
        self.password = password

    def set_destination(self, destination):
        """
        Sets destination.
        :param destination:list of strings
        :return:None
        """
        assert(type(destination) == list), 'Destination type should be list.'
        self.destination = destination

    def get_destination(self):
        """
        Returns destination list.
        :return:list of strings
        """
        return self.destination

    def get_sender(self):
        """
        Returns sender email and password.
        :return:list of strings
        """
        return [self.sender, self.password]
