# AI and Workflow Automation

This repository contains Python scripts and n8n workflows for student-data ETL, Google Sheets and Gmail automation, Telegram integrations, and Slack automation.

## Project contents

### Python

| File | Description |
| --- | --- |
| `etl_cleaner.py` | Uses OpenAI to clean student enrollment records from a CSV file and save the results. |
| `google-sheet-to-gmail-automation.py` | Reads rows from a Google Sheet, prints them, and sends a test email with the Gmail API. |
| `student_enrollment_raw.csv` | Sample student enrollment input data. |
| `students_cleaned.csv` | Sample cleaned student enrollment output. |

### n8n workflows

Import a workflow JSON file into n8n, then configure the credentials required by its nodes.

| Workflow file | Description |
| --- | --- |
| `n8n/ETL AI Automation - Learning.json` | Accepts a CSV through a form, cleans student records with an OpenAI model, and routes the results to file outputs. |
| `n8n/ETL AI Automation - Summarize Google Sheet Data.json` | Reads Google Sheets data, summarizes it with OpenAI, and sends the result through Telegram. |
| `n8n/ETL AI Automation - Telegram - GMail.json` | Processes a Telegram-triggered request with OpenAI and sends an email through Gmail. |
| `n8n/Google Sheets to GMail.json` | Reads Google Sheets rows and sends email through Gmail, with conditional routing. |
| `n8n/Slack Automation - Initial step.json` | Starter Slack workflow using a webhook and a Slack message action. |
| `n8n/Slack Receipe Bot.json` | Slack-triggered recipe bot that uses OpenAI and replies in Slack. |

The workflows are inactive when imported. Configure the required Google Sheets, Gmail, OpenAI, Telegram, or Slack credentials in n8n, then test and activate each workflow as appropriate.

### Screenshots

- `ETL Automation using python.png` — Python student-data ETL.
- `Google Sheet to Gmail Automation - python.png` — Python Google Sheets and Gmail automation.
- `n8n/Student Clean up with n8n.png` — Student cleanup workflow.
- `n8n/Google Sheet to Gmail Automation - n8n.png` — Google Sheets to Gmail workflow.
- `n8n/Summarize Google Sheet.png` — Google Sheets summary workflow.
- `n8n/slack receipe bot.png` — Slack recipe bot.
- `n8n/Cutomized Emil Sender.png` — Customized email sender.

## Python student-data ETL

### Requirements

- Python 3
- An OpenAI API key

Create and activate a virtual environment from the project directory:

```bash
python -m venv .venv
```

On Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install pandas openai python-dotenv
```

Create a `.env` file in the project directory:

```dotenv
OPENAI_API_KEY=your_openai_api_key
```

Run the ETL script:

```bash
python etl_cleaner.py
```

By default, the script reads `student_enrollment_raw.csv` and writes `students_cleaned.csv` in the current directory. Change `INPUT_CSV` and `OUTPUT_CSV` at the bottom of `etl_cleaner.py` to use different paths. The script sends the student data to OpenAI using the `gpt-4o-mini` model.

The expected CSV columns are `Student_ID`, `Name`, `Email`, `Phone`, `Course`, `Fee_Paid`, `City`, and `Enrolled_Date`. The cleaning prompt asks the model to standardize names and cities, validate emails and phone numbers, normalize course names and payment values, and format enrollment dates as `YYYY-MM-DD`.

## Python Google Sheets to Gmail automation

### Requirements

- Python 3
- A Google Cloud project with the Google Sheets API and Gmail API enabled
- OAuth desktop-app credentials saved as `credentials.json`

Install the Python dependencies:

```bash
python -m pip install gspread google-api-python-client google-auth google-auth-oauthlib
```

Run the script:

```bash
python google-sheet-to-gmail-automation.py
```

On first run, the script opens a browser for Google account authorization and saves the resulting OAuth token in `token.json`. It then reads and prints rows from the spreadsheet configured by `SPREADSHEET_ID` and sends a test email to the recipient configured in the script. Update those values in `google-sheet-to-gmail-automation.py` before running it with your own spreadsheet and recipient.

## n8n setup

1. Open your n8n instance and import the desired workflow JSON file from `n8n/`.
2. Set up the credentials required by the workflow's nodes.
3. Review and update workflow-specific values, such as sheet selection, recipients, and trigger settings.
4. Test the workflow with non-sensitive sample data before activating it.

The student ETL workflow uses an upload form and an OpenAI Chat Model node. The other workflows integrate with their respective Google Sheets, Gmail, Telegram, OpenAI, or Slack services. Their trigger types and outputs differ, so review each workflow in the n8n editor before enabling it.

## Privacy and credentials

The ETL scripts and AI-enabled workflows send data to external services such as OpenAI, Google, Telegram, or Slack. Process only data you are authorized to share, and follow your organization's privacy requirements.

Keep API keys, OAuth credentials, and tokens in local environment files or service credential stores. Do not commit `.env`, `credentials.json`, `token.json`, or real personal data to the repository.
