import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from .logs import logger

QQ_SMTP_HOST = "smtp.qq.com"


class EmailClient(object):

    def __init__(self, server_host, sender, sender_name, password):
        self.server_host = server_host
        self.sender = sender
        self.sender_name = sender_name
        self.password = password

    def send(self, subject, body, receivers):
        ret = True
        try:
            msg = MIMEText(body, 'html', 'utf-8')
            msg['From'] = formataddr((self.sender_name, self.sender))
            msg['To'] = formataddr((','.join(receivers), ','.join(receivers)))
            msg['Subject'] = subject

            server = smtplib.SMTP(self.server_host, 25)
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, receivers, msg.as_string())
            server.quit()
        except Exception as e:
            logger.error(e)
            ret = False
        return ret


class QQEMailClient(EmailClient):

    def __init__(self, sender, sender_name, password):
        super().__init__(QQ_SMTP_HOST, sender, sender_name, password)
