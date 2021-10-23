import FetchEmail
import secrets
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
        result = slackClient.files_upload(
            channels=secrets.slack_channels,
            initial_comment=initialComment,
            file=attachment,
        )
    else:
        result = slackClient.files_upload(
            channels=secrets.slack_channels,
            file=attachment,
        )


slack_token = secrets.slack_token

imapConnection = FetchEmail.FetchEmail(secrets.serverName,secrets.username,secrets.password)
imapConnection.select_folder(secrets.usps_folder)

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
    imapConnection.move_message(message,secrets.archive_folder)

imapConnection.connection.close()





