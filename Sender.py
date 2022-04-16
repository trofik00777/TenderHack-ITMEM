import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Sender:
    def __init__(self, receiver_email, sender_email: str = "thefroggylovers@gmail.com",
                 password: str = "a4+hPuC!X5j_tQKk*9geaQB"):
        self.sender_email = sender_email  # Enter your address
        self.password = password
        self.receiver_email = receiver_email

    def sendMessage(self, html):
        print("Start send mail")
        message = MIMEMultipart("alternative")
        message["Subject"] = "!!!Attention!!!"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        part1 = MIMEText(html, "html")
        message.attach(part1)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())
        print("We end send email")

    def template(self, status: int, href: str):
        html = ""
        if (status == 1):
            html = f"""\
                <html>
                  <body>
                    <p>You are win,<br>
                       Check you progress in 
                       <a href="{href}">click</a>
                    </p>
                  </body>
                </html>
                """
        elif (status == 2):
            html = f"""
                    <html>
                      <body>
                        <p>We go out from this catsession,<br>
                           Too low many for you which you can earn =(. Saw you progress in 
                           <a href="{href}">click</a>
                        </p>
                      </body>
                    </html>
                    """
        else:
            print("Problem with sender")
        self.sendMessage(html)
