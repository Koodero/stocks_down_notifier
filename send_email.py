import smtplib
from dotenv import load_dotenv
import os

# Sending email
def send_gmail(stock, date, procent):

    email_subject = "Stocks are down at least 15%"
    message = (
        f"Your stock {stock} has gone down {procent:.2f}% from the date {date}."
    )

    load_dotenv() 

    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=os.getenv("SENDER_MAIL"), password=os.getenv("SENDER_MAIL_PASS"))
                connection.sendmail(
                    from_addr=os.getenv("SENDER_MAIL"), 
                    to_addrs=os.getenv("RECIEVER_MAIL"),
                    msg=f"Subject:{email_subject}\n\n{message}".encode("utf-8")
                )
        print(f"Email sent to {os.getenv('RECIEVER_MAIL')}")
                
    except smtplib.SMTPException as e:
        print(f"Failed to send email to {os.getenv('RECIEVER_MAIL')}: {e}")
    except Exception as e:
        print(f"An error occurred while sending email to {os.getenv('RECIEVER_MAIL')}: {e}")


# SENDER_MAIL and RECIEVER_MAIL can be same
# SENDER_MAIL_PASS - sender gmails google app password