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
            print("All emails sent successfully!")
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

    TODO: refactor to make it use key value pairs and then return the assignments for easier testing
          and to remove the message creation from the assignment logic.
'''
def create_assignment_list(recipients, debug=False):
    assignees = recipients.copy()
    messages = []
    i = 0
    while i <= len(recipients) + 2:
        # print('iteration',i)
        receiver_email = assignees[i]
        current_recipient = recipients[random.randint(0, len(recipients) - 1)]
        while current_recipient == receiver_email:
            if len(recipients) == 1:
                print("Last recipient is the same as sender, restarting assignment...")
                messages.clear()
                recipients = assignees.copy()
                current_recipient = None
                print("Recipients reset:", recipients)
                print("Assignees:", assignees)
                i = 0  
                break
            current_recipient = recipients[random.randint(0, len(recipients) - 1)]
        if current_recipient is not  None:
            recipients.remove(current_recipient)
            body = f"You have been assigned {current_recipient} for Secret Santa! Keep it a secret!"
            messages.append(create_email(receiver_email, body))
            i += 1
        else:
            continue
        if debug:
            print(f"Assigned {current_recipient} to {receiver_email}")
    print("Final assignments:")
    for msg in messages:
        print(msg['To'] + " --> " + msg.get_content().split()[4]) 
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

    # recipients = get_recipients()
    recipients = ['kikuforrest@gmail.com', 'laurentforrest596@gmail.com','elli.rose.forrest@gmail.com','thekinghobbit@gmail.com']
    messages = create_assignment_list(recipients, debug=True)
    # send_email_list(messages)

if __name__ == "__main__":
    __main__()