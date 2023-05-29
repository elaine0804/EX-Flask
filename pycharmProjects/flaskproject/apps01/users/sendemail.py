import email.message
import smtplib

def sendmail(gemail,pwd):
    msg = email.message.EmailMessage()
    msg["From"] = "elainechen278@gmail.com"
    msg["To"] = gemail
    msg["Subject"] = "登入驗證信"
    msg.set_content("登入驗證碼為"&pwd)
    #msg.add_alternative("<h3>HTML內容</h3>安安這是寄送郵件測試",subtype="html") #HTML信件內容
    acc = "elainechen278@gmail.com"
    password = "zlekvrbzngxqwtra"
    server = smtplib.SMTP_SSL("smtp.gmail.com",465) #建立gmail連線
    server.login(acc, password)
    server.send_message(msg)
    server.close()