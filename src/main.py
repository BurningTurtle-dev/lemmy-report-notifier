from pythorhead import Lemmy

import pyotp
from time import sleep
import os
import requests

lemmy_url = os.environ['LEMMY_URL']
username = str(os.environ['LEMMY_USERNAME']).encode('unicode-escape').decode()
password = str(os.environ['LEMMY_PASSWORD']).encode('unicode-escape').decode()
totp = os.environ['LEMMY_TOTP']
ntfy_url = os.environ['NTFY_URL']
pulling_frequency = int(os.environ['PULLING_FREQUENCY'])
timeout = int(os.environ['TIMEOUT'])

sent_reports = list()

"""
This function sends a message to a ntfy url.
"""
def send_message(message: str) :
    request = requests.post(ntfy_url, data=message)

"""
This function get all nessessary information from the Lemmy server
"""
def get_info() -> list :
    messages = list()

    reports_posts = lemmy.post.report_list(unresolved_only="true")
    reports_comments = lemmy.comment.report_list(unresolved_only="true")
    reports = reports_comments + reports_posts

    unresolved_reports = list()

    for report in reports:
        community_name = report.get("community").get("title")
        report_id = int

        if report.get("comment_report") is not None:
            report_id = int(report.get("comment_report").get("id"))
        else :
            report_id = int(report.get("post_report").get("id"))
        
        unresolved_reports.append(report_id)

        if not any(i == report_id for i in sent_reports):
            messages.append('You recieved a new report in \"%s\" on \"%s\"' %(community_name, lemmy_url))
    sent_reports.clear()
    sent_reports.extend(unresolved_reports)
    return messages

print("started")
lemmy = Lemmy(lemmy_url,request_timeout=timeout)

if totp is None:
    lemmy.log_in(username, password)

else:
    lemmy.log_in(username, password, pyotp.TOTP(totp).now())

while True:
    formated_messages = get_info()
    for message in formated_messages:
        send_message(message)
    sleep(pulling_frequency)