from pythorhead import Lemmy

import pyotp
import time
import os
import requests

lemmy_url = os.environ['LEMMY_URL']
username = os.environ['LEMMY_USERNAME']
password = os.environ['LEMMY_PASSWORD']
totp = os.environ['LEMMY_TOTP']
ntfy_url = os.environ['NTFY_URL']
pulling_frequency = int(os.environ['PULLING_FREQUENCY'])

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
    sent_reports = list()

    reports_posts = lemmy.post.report_list(unresolved_only="true")
    reports_comments = lemmy.comment.report_list(unresolved_only="true")
    reports = reports_comments + reports_posts

    for report in reports:
        community_name = report.get("community").get("title")
        messages.append('You recieved a new report in \"%s\" on \"%s\"' %(community_name, lemmy_url))

        report_id = int

        #TODO not printing the id
        if report.get("comment_report") is not None:
            report_id = int(report.get("comment_report").get("id"))
        else :
            report_id = int(report.get("post_report").get("id"))
        print(report_id)


    
    return messages

lemmy = Lemmy(lemmy_url,request_timeout=2)

if totp is None:
    lemmy.log_in(username, password)

else:
    lemmy.log_in(username, password, pyotp.TOTP(totp).now())

while True:
    formated_messages = get_info()
    for message in formated_messages:
        send_message(message)
    
    time.sleep(pulling_frequency)