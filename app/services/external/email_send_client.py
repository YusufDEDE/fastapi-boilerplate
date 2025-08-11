import smtplib
from email.message import EmailMessage
from typing import List, Optional


class EmailSendClient:
    def __init__(
            self,
            smtp_host: str,
            smtp_port: int,
            username: str,
            password: str,
            use_tls: bool = True,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send_email(
            self,
            subject: str,
            body: str,
            to_emails: List[str],
            cc_emails: Optional[List[str]] = None,
            bcc_emails: Optional[List[str]] = None,
            html: bool = False,
    ) -> None:
        from_email = self.username

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = ", ".join(to_emails)

        if cc_emails:
            msg["Cc"] = ", ".join(cc_emails)

        recipients = to_emails + (cc_emails or []) + (bcc_emails or [])

        if html:
            msg.add_alternative(body, subtype="html")
        else:
            msg.set_content(body)

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            if self.use_tls:
                server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg, from_addr=from_email, to_addrs=recipients)
