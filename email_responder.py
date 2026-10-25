#Importing the necessary libraries.
import os
from groq import Groq
from email.message import EmailMessage
from imap_tools import MailBox, AND
import smtplib
from dotenv import load_dotenv
import time

#loading the environment that stores the api key and the password for the email.
load_dotenv()

#Saving the mail username and the mail password to local values that I will be needing in the future.
#The password is being obtained from the .env file. 
MAIL_USERNAME = "od.grok.bot.test@gmail.com"
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

#Defining the function that sends the api request to an LLM. 
#The LLM I am using is groq and the model is gpt-oss-120b. It supports up to 1k tokens (requests) daily. 
def ai_process(REQUEST) : 

    #Setting the client via the api key
    client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

    #Making the api request
    chat_completion = client.chat.completions.create(

        #Defining the message.
        #We put two parameters here : 1)With a role "system" that tells the LLM what purpose it solves and gives it specific instructions.
        #                             2)With a role "user" that gives the request to the LLM and the necessary information.
        messages=[
            {
                "role" : "system",

                "content" : "You are the official automated email assistant for Odyceo. Your task is to read the incoming email and draft a polite, professional, and helpful reply "
                            "on behalf of the team. Maintain a formal yet welcoming tone. Do not invent unverified information about Odyceo's operations or procedures. "
                            "Sign off simply as 'The Odyceo Team'. Always write your response in the exact same language as the sender's original email."
                            "Under no circumstances should you include any URLs, website links, or placeholder email addresses in your response."
                            "Keep your response concise, brief, and strictly under 3 short paragraphs."
            },
            
            {
                "role": "user",

                "content": f"The date the email was sent is {REQUEST[1]}, the subject of the email is {REQUEST[2]} and the email you have to reply to is {REQUEST[3]}" ,
            }
        ],

        #Defining the model 
        model="openai/gpt-oss-120b",

        #Setting the temperature of the model. The value 0.3 is placed so that we can have little creativity from our model and be sure that 
        #the same questions have the same answers. 
        temperature = 0.3,

        #Setting the max tokens of the output to 1024 so that the model can provide a full answer.
        max_tokens= 1024
       )

    #Finally we are returning the answer.
    return (chat_completion.choices[0].message.content)


#Defining the function that sends the email. It takes three values : 
#TO_REQ : To whom we are sending the email.
#SUBJECT_REQ : The subject of the answer.
#TEXT_REQ : The body text of the answer.
def export_email(TO_REQ , SUBJECT_REQ , TEXT_REQ):

    #Creating a msg object from the email.message library that makes the process of writing the email easier.
    msg = EmailMessage()

    #Setting the subject
    msg["Subject"] = SUBJECT_REQ

    #Setting the From atribute.
    msg["From"] = MAIL_USERNAME

    #Setting the To atribute.
    msg["To"] = TO_REQ

    #Setting the content of the email. 
    msg.set_content(TEXT_REQ)


    #Making the process that sends the email
    with smtplib.SMTP("smtp.gmail.com", 587 ) as smtp: 

        #Establishing connection with the server.
        smtp.starttls()

        #Logging in to the email. 
        smtp.login(MAIL_USERNAME , MAIL_PASSWORD)

        #Sending the email.
        smtp.send_message(msg)
    

#Defining the function that reads the email processes it with the ai function and then sends the response.
def read_email() : 
    
    #Using the Mail Box function from the imap tools library to login to our email and specifically to our inbox.
    with MailBox("imap.gmail.com").login(MAIL_USERNAME , MAIL_PASSWORD , initial_folder = "Inbox") as mb:

        #Setting a loop to read every unseen email.
        for msg in mb.fetch(AND(seen=False)) :

            #Obtaining the email of the sender.
            from_request = msg.from_

            #Filtering the emails that specifically should not be replied to.
            if "noreply" in from_request or "no-reply" in from_request or "donotreply" in from_request :
                continue

            #Obtaining the subject of the email.
            subject_request = msg.subject

            #Obtaining the text of the email(text form or HTML form).
            text_request = msg.text or msg.html

            #Obtaining the date that the email has been sent.
            date_request = msg.date

            #Setting the request list that stores the email's information needed for the LLM.
            request = [from_request , date_request , subject_request , text_request]

            #Calling the ai_process function on the request list
            Reply = ai_process(request)

            #Exporting the email
            export_email(from_request , f"Re: {subject_request}" , Reply )

#Setting a loop that runs in the backround so that while the program is running the emails are beeing read.
while True:
    try:

    #Starting the whole process.
        read_email()

    #With the next line of code the program doesn't stop even if there is an internet problem. 
    except Exception:
        pass

        #Stops for 60 seconds before checking the next email.  
        time.sleep(60)
            

 