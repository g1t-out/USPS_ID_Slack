import FetchEmail
import slack_sdk
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import datetime


def post_slack_image(attachment: str, initialComment: str = "") -> None:
    """
    Takes an attachment path and posts it to Slack.
    If Initial Comment is set, it will post that
    """
    if initialComment != "":
        result = slackClient.files_upload_v2(
            channel=slack_channel,
            initial_comment=initialComment,
            file=attachment,
        )
        assert result["file"]
    else:
        result = slackClient.files_upload_v2(
            channel=slack_channel,
            file=attachment,
        )
        assert result["file"]

serverName = os.environ['serverName']
username = os.environ['username']
password = os.environ['password']
usps_folder = os.environ['usps_folder']
archive_folder = os.environ['archive_folder']
slack_token = os.environ['slack_token']
slack_channel = os.environ['slack_channel']

imapConnection = FetchEmail.FetchEmail(serverName,username,password)
imapConnection.select_folder(usps_folder)

messages = imapConnection.fetch_messages()

firstSlack = True

for message in messages:
    attachments = imapConnection.save_attachments(message)
    for attachment in attachments:
        if firstSlack:
            firstSlack = False
            slackClient = WebClient(token=slack_token)
            post = "USPS Letters for " + str(datetime.date.today())
            post_slack_image(attachment,post)
        else:
            post_slack_image(attachment)
    imapConnection.move_message(message,archive_folder)

imapConnection.connection.close()





