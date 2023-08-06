import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header


class Email:
    def __init__(self, email_account: str, email_password: str, email_to: str,
                 email_title='', email_content='', file_list=None):
        """
        a simple send email method
        """
        server = smtplib.SMTP('smtp.qq.com')
        message = MIMEMultipart()  # email body
        print("sending email...")
        email_title = email_title if email_title else "Test Report!"
        email_content = email_content if email_content else 'Your test result has been generated. Please check the attachment for details!\n'

        # set email
        message['From'] = Header(f"<{email_account}>", 'utf-8')
        message['Subject'] = Header(email_title, 'utf-8')
        message.attach(MIMEText(email_content))

        if file_list:
            for file in file_list:
                try:
                    file_apart = MIMEApplication(open(file, 'rb').read(), file.split('.')[-1])
                    file_apart.add_header('Content-Disposition', 'attachment', filename=file.split("\\")[-1])
                    message.attach(file_apart)
                except Exception as e:
                    print("wrong file %s %s" % (file, str(e)))

        # send email to someone
        try:
            server.login(email_account, email_password)
            server.sendmail(email_account, email_to, message.as_string())
            print("Mail sent successfully! addressee:" + str(email_to))
            server.quit()
        except smtplib.SMTPException as e:
            print('Mail sending failed! Error message:' + str(e))
