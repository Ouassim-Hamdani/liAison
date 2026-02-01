import json
from agents.dispatcher.agent import DispatcherAgent
from pprint import pprint
agent = DispatcherAgent()
def analyze_emails():
    EMAILS_DB = "C:\\Projects\\Hack in saclay\\Smart Claims Management\\data\\emails.json"
    with open(EMAILS_DB, "r", encoding="utf-8") as f:
        emails = json.load(f)
    for email in emails:
        response = agent.invoke(email['subject'] + "\n\n" + email['body'])
        # add class to data 
        email['department'] = response.department.value
        email['urgency'] = response.urgency.value
    return emails
if __name__ == "__main__":
    pprint(analyze_emails())
        