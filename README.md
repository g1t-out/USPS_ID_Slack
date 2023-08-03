# USPS_ID_Slack

The purpose of this script is to read a specific folder in an email account (via IMAP) and to take the attachments from that email and post them to Slack. In my case, I'm using it on the USPS Informed Delivery emails which then attaches images of my incoming mail in a Slack channel. This can be used for any type of file, but I've only tested it with PNG and PDFs, both of which worked. Now I know that I can just setup forwarding rules to send these emails to whoever needs to receive them, but it isn't as cool as posting them to Slack.

## Necessary Environment Variables

* serverName : IMAP server to connect to
* username : Username to connect to IMAP server with
* password : Password to connect to IMAP server with
* usps_folder : Folder that the script looks in the mailbox for new messages
* archive_folder : Location to move an email to after we've sent its attachments to Slack
* slack_token : OAuth token for your workspace (See below for how to generate this)
* slack_channel : Slack channel to post this in. This needs to be the ID of the channel and not the name of the channel. This can be found by browsing the Slack instance with a browser then clicking on the channel, then copying everything after the last forward slash (/)


## Creating an App with Necessary Permissions

1. Browse to [Slack's API Page](https://api.slack.com)
1. Click "Your Apps" in the Upper left
1. CLick "Create New App"
1. Choose "From scratch"
1. Give the App a name and choose your workspace
1. Click "Permissions"
1. Under "Scopes" click "Add an Oauth Scope"
1. Add "files:write" and "files.read"
1. Click "Install to workspace"
1. The "Bot User OAuth Token" that is now displayed should be the `slack_token` environment variable
1. Browse to the channel you would like the bot to post in. Right click on the channel and click "View Channel Details"
1. Click "Integrations"
1. Under "Apps", click "Add an App"
1. Find your app and click "Add"