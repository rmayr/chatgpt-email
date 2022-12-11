# chatgpt-email
This is the start of a small bot that uses ChatGPT to answer (spam) emails.

## Setup
For e.g. postfix, piping incoming email to a (virtual) user email address should be as simple as adding a line to /etc/aliases:
chatterbox: "| /usr/local/bin/emailbot.py /etc/local/emailbot/config.json /var/log/emailbot.log"

Then adapt config.json from config.json.template to fill in your query prompt file and login details for ChatGPT.
