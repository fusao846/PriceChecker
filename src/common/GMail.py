# ライブラリ設定
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders
from pathlib import Path
import os

def send_gmail(password, mail_from, mail_to, subject, message, img):
    # メール情報の設定
    # MIMEマルチパートでメールを作成
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = mail_to
    msg['From'] = mail_from
    msg.attach(MIMEText(message))
    if img != '':   
        attach_file = {
            'name':os.path.basename(img),
            'path':img
        }
        attachment = MIMEBase('image', 'png')
        file = open(img, 'rb+')
        attachment.set_payload(file.read())
        file.close()
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=img)
        msg.attach(attachment)

    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_password = password

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        #サーバー・ポート接続
        server.ehlo()
        # TLS暗号化
        server.starttls()
        # SMTPサーバーログイン
        server.login(mail_from, smtp_password)
        server.send_message(msg)
        #SMTPサーバー遮断
        server.quit()
    except Exception as e:
        print('exception')
        print(e)
        return {
            "status":"ERROR",
            "message":str(e)
        }
    return {
        "status":"OK",
        "message":""
    }
