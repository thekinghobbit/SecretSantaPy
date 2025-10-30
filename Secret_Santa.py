import smtplib
import os
import random
import time
from dotenv import load_dotenv
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

load_dotenv()
random.seed(time.time())

SENDER_EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

'''
send_email_list(messages):
    Sends a list of email messages using SMTP.
    input: messages - list of EmailMessage objects
    output: None
'''
def send_email_list(messages):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, PASSWORD)
            for message in messages:
                server.send_message(message)
    except Exception as e:
        print(f"An error occurred while sending emails: {e}")
'''
create_email(receiver_email, body):
    Creates an email message.
    input: receiver_email - recipient's email address
           body - body of the email
    output: EmailMessage object
'''
def create_email(receiver_email, body):
    message = EmailMessage()
    message['From'] = SENDER_EMAIL
    message['To'] = receiver_email
    message['Subject'] = "Secret Santa Assignment"
    message.set_content(body)
    return message
'''
create_assignment_list(recipients):
    Creates a list of email messages assigning Secret Santa recipients.
    input: recipients - list of recipient email addresses
    output: list of EmailMessage objects
'''
def create_assignment_list(recipients):
    assignees = recipients.copy()
    messages = []
    for i in range(len(recipients)):
        receiver_email = assignees[i]
        current_recipient = recipients[random.randint(0, len(recipients) - 1)]
        while current_recipient == receiver_email:
            if len(recipients) == 1:
                print("Last recipient is the same as sender, restarting assignment...")
                return create_assignment_list(recipients)
            current_recipient = recipients[random.randint(0, len(recipients) - 1)]

        recipients.remove(current_recipient)
        # recipients = [receiver_email] + recipients
        body = f"You have been assigned {current_recipient} for Secret Santa! Keep it a secret!"
        messages.append(create_email(receiver_email, body))
    return messages

'''
get_number_of_recipients():
    Prompts user for number of recipients and validates input.
    input: gets user input from console
    output: int - number of recipients
'''
def get_number_of_recipients():
    number_of_recipients = input("Enter number of recipients: ")
    while not number_of_recipients.isdigit() or int(number_of_recipients) <= 0:
        number_of_recipients = input("Please enter a valid positive integer for number of recipients: ")
    return int(number_of_recipients)

''' 
get_recipients():
    Prompts user for recipient email addresses and confirms the list.
    input: gets user input from console
    output: list of recipient email addresses
'''
def get_recipients():
    number_of_recipients = get_number_of_recipients()
    recipients = []
    for i in range(int(number_of_recipients)):
        recipient_email = input(f"Enter email address for recipient {i + 1}: ")
        recipients.append(recipient_email)
    print("Recipients:", recipients)
    confirm = input("Is this correct? (y/n): ")
    while confirm.lower() not in ['y', 'n']:
        confirm = input("Please enter 'y' for yes or 'n' for no: ")
    if confirm.lower() != 'y':
        return get_recipients()
    return recipients
     
def __main__():

    recipients = get_recipients()
    messages = create_assignment_list(recipients)
    send_email_list(messages)

if __name__ == "__main__":
    __main__()