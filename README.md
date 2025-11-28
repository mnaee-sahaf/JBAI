# JBAI

AI & Automation Engineer - Candidate Assignment
This assignment contains three small tasks related to Python coding, automation, and AI
workflows. You can complete all tasks in 3–5 hours in total. Please use only fake/sample
data – do not include any real customer data.
Task 1 – Python Coding: Mini Time-Tracking Data Pipeline + Power BI Analysis
Create a CSV file named raw_time_entries.csv containing 20 rows of fake data with the
columns:
user_id, organization_id, time_in, time_out, device, currency, amount
Example rows (you can create your own fake data, make sure you have at least 4 types of
currencies and at least 5 rows are missing time in or time out cells):
101,501,2025-01-01T09:02:00,2025-01-01T17:01:00,web,MYR,34
101,501,2025-01-02T09:05:00,2025-01-02T16:59:00,mobile,USD,12
205,220,2025-01-01T10:00:00,2025-01-01T18:15:00,ios,PHP,900

Your task:
Create a Python script named clean_pipeline.py
The script should do:
1. Data cleaning
• Remove rows where time_in or time_out is missing.
• Normalize device values to one of: WEB, MOBILE, IOS, ANDROID.
2. Transformations
• Compute duration_minutes = time_out - time_in (in minutes).
• Convert the amount column into USD using a fixed rate dictionary defined inside the script
3. Outputs
• Save a new file clean_entries.csv with the columns:
user_id, organization_id, date, duration_minutes, device, amount_usd
• Generate a report.json file with the structure:
{
"total_entries": ...,
"clean_entries": ...,
"avg_duration": ...,
"total_amount_usd": ...
}|

4. Power BI analysis
• Import clean_entries.csv into Power BI Desktop.
• Create at least three visuals, for example:
- A bar chart showing average duration_minutes per user_id.
- A bar or column chart showing total amount_usd per organization_id.
- A stacked column chart showing total duration_minutes by device.
• (Optional) Create one DAX measure (e.g. total_amount_usd or avg_duration_minutes) and
use it in a visual.
Deliverables (use a google drive link for all tasks – name each file with task1, task2 or
task3 in front):
• clean_pipeline.py
• raw_time_entries.csv
• clean_entries.csv
• report.json
• your .pbix file

Task 2 - Automation (Make.com): Payment Failure Alert Simulation
Build a simple scenario in Make.com (free account) that simulates how a payment failure
alert flow would work. You do not need any external integrations other than Make.com
itself.
Your task:
1. Initial data (Set variable)
• Add a module: Tools → Set variables.
• Create variables with the following fields and values (you may adjust the values):
{
"customer": "Abcde Corp",
"plan": "Pro Annual",
"amount": 999,
"currency": "USD",
"status": "payment_failed"
}
2. Branching logic (Router)
• Add a Router after the Set variable module.
• On one route, continue only if status = payment_failed.
• On the other route (status ≠ payment_failed), simply end the flow (no further action).
3. Create alert message
• On the payment_failed route, create a text message that looks like:
ALERT: Payment failed
Customer: {{customer}}
Plan: {{plan}}
Amount: {{amount}} {{currency}}
Timestamp: {{now}}
4. Create a webhook to send a notification – with Alert: Payment failed – your name,
customer name and status - use this URL – to get a webhook URL - https://webhook.site/
Extra step (step 5) – do it only if you are cool! (you need to read documentation)
5. Email output
• Use Make.com’s built-in Email module (Gmail required) to send the alert to your own
email address.
• The subject should be something like: Payment failed alert for {{customer}}.
Deliverables:
• Screenshot of the full scenario in Make.com (before and after you run it once, make sure to
click the last running notification from the right upper corner of the last module that
worked)
• Exported blueprint (JSON)
• Link to the webhook – from webhook.site
• Screenshot with the received email
• A short (4–6 sentences) explanation of how the flow works


Task 3 – AI Task: Classify Support Messages
In this task you will classify fake support tickets into categories using a free AI installed on
your machine.
Use the following 20 fake support messages:
1. The app is not tracking my time on Android anymore.
2. I would like to upgrade my plan from Free to Pro.
3. How can I export all my timesheets to Excel?
4. Billing failed again, my credit card keeps getting declined.
5. I forgot my password and cannot log in.
6. The web dashboard is very slow when loading reports.
7. Can you add an integration with Microsoft Teams?
8. I want to change the owner of our workspace.
9. The mobile app crashes every time I try to clock in.
10. How do I invite new members to my organization?
11. We were charged twice this month, please check our invoice.
12. Is there a way to track time offline and sync later?
13. Please add dark mode to the web app.
14. I need help updating our company billing address.
15. The GPS location is inaccurate when my team clocks in.
16. Can I limit which devices employees are allowed to clock in from?
17. Our data export is missing some projects.
18. I’d like to request a feature to approve timesheets before payroll.
19. My account was deactivated and I don’t know why.
20. We need an option to automatically round time entries to 15 minutes.
You can either copy these messages into a file named messages.txt (one message per line)
or read them directly from your script.


Your task:
• Create a Python script named classify_tickets.py that:
1. Reads each message (either from messages.txt or from a list inside the script).
2. Sends the text to the AI model on your machine.
3. Performs zero-shot classification using the following labels: bug, billing, feature_request,
account_help, other.
4. For each message, chooses the label with the highest score and writes the results to a file
classified_local.json with entries like:
[
{
"text": "...",
"category": "...",
"score": 0.95
},
...
]

5. Prints a summary in the terminal with counts per category, for example:
Total: 20
Bug: 7
Billing: 3
Feature Request: 4
Account Help: 4
Other: 2



Deliverables
Submit:
• classify_local_ai.py
• classified_local.json
• A short README describing:
o which model you installed
o how to install dependencies
o how to run the script
