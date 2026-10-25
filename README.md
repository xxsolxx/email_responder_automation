# Automated Email Responder case 

An automated, Python-based email assistant designed for Odyceo. This script continuously monitors a Gmail inbox for unread messages and leverages the Groq API (Llama 3) to draft and send polite, professional, and context-aware replies on behalf of the team.

## Key Features
* **Continuous Background Monitoring:** Automatically checks the inbox every 60 seconds without manual intervention.
* **AI-Powered Replies:** Uses Groq's API to understand incoming emails and generate tailored, professional responses.
* **Smart Threading:** Replies directly within the original email thread (using the `Re: ` prefix).
* **Spam/Bot Protection:** Intelligently ignores automated senders (e.g., `noreply`, `donotreply`).
* **Resilient Execution:** Built-in error handling prevents the script from crashing during temporary network drops.

## Prerequisites
* Python 3. installed.
* A Gmail account with an **App Password** generated (standard account passwords will not work for IMAP/SMTP).
* A Groq API Key.

##  Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/email_responder_automation.git](https://github.com/your-username/email_responder_automation.git)
   cd email_responder_automation
   
2. **Install the required dependencies:**

    ```bash
    pip install groq imap_tools python-dotenv

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and securely add your credentials:
   
    MAIL_PASSWORD="your-gmail-app-password"
   
    GROQ_API_KEY="your-groq-api-key"

*(Note: The `.env` file is ignored via `.gitignore` to keep your credentials safe.)*

## Usage

**Standard Execution (Terminal):**

    python email_responder.py

**Background Execution (Windows):**
To run the script silently in the background without keeping a terminal window open:
1. Rename `email_responder.py` to `email_responder.pyw`.
2. Double-click the file to start the background process. 
3. *To stop the script:* Open Task Manager (`Ctrl + Shift + Esc`), locate the "Python" process, and click "End task".

   
