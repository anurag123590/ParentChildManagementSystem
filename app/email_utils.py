import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(receiver_email, subject,body):
    sender_email = "anuragpp28@gmail.com" 
    password = "cfimilzlrvttrxwc"  
    smtp_server = "smtp.googlemail.com"  
    smtp_port = 465

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
   

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
       
        
        server.login(sender_email, password)
        print('yahoooo sending')
        server.sendmail(sender_email, receiver_email, message.as_string())
        print('yahooo done')
        server.quit()
        print("Activation email sent successfully")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error sending activation email: {str(e)}")


#