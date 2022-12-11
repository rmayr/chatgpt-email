#!/usr/bin/python3

from revChatGPT.revChatGPT import Chatbot
import json
import email
import smtplib
import logging
import sys
from email.message import EmailMessage

# example from https://pythonexamples.org/python-logging-debug/
logger = logging.getLogger('chatgpt-email')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('emailbot.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# example from https://github.com/acheong08/ChatGPT
configfile = open("config.json", "r")
config = json.load(configfile)
logger.debug("Using login data: " + config['email'] + " / " + config['password'])

promptfile = open('queryprompt.txt', 'r')
queryprompt = promptfile.read()
logger.debug("Prompt query for priming ChatGPT session: " + queryprompt)

newmsg = email.message_from_file(sys.stdin)
logger.debug("Processing new incoming email message: " + newmsg.as_string())

replyaddr = newmsg['From']
if (not replyaddr):
    replyaddr = newmsg['Reply-To']
if (not replyaddr):
    replyaddr = newmsg['Return-Path']
if (not replyaddr):
    sys.exit("Unable to parse email message for from/reply-to/return-path address")
    
receivedaddr = newmsg['To']
if (not receivedaddr):
    receivedaddr = newmsg['Delivered-To']
if (not receivedaddr):
    receivedaddr = config['spamtrap']
if (not receivedaddr):
    sys.exit("Unable to parse email message for to/delivered-to address and fallback spamtrap address not configured")

subject = newmsg['Subject']
if (not subject):
    subject = "your message"

messageid = newmsg['In-Reply-To']
if (not messageid):
    messageid = newmsg['References']
if (not messageid):
    messageid = newmsg['Message-ID']

logger.info("New incoming message to '" + receivedaddr + "' from '" + replyaddr + "' with message-id '" + messageid + "', subject: " + subject)

# TODO: store some state to tie the new conversation_id in with messageid for continuing future conversations
chatbot = Chatbot(config, conversation_id=None)
#chatbot.reset_chat() # Forgets conversation
chatbot.refresh_session() # Uses the session_token to get a new bearer token
resp = chatbot.get_chat_response(queryprompt, output="text")
logger.debug("Response to query prompt: " + resp['message']) # The message sent by the response
#resp['conversation_id'] # The current conversation id
#resp['parent_id'] # The ID of the response

# this shortcut is no longer supported in the email class it seems
#msgbody = newmsg.get_body('plain')
# use the long way around
for m in newmsg.walk():
    if m.get_content_subtype()=='plain':
        try:
            msgbody = str(m.get_payload(decode=True),encoding='utf-8')
            logger.debug("Parsed email message body: " + msgbody)
        except:
            sys.exit("Unable to parse email message for text/plain part")

# and finally create reply message
replymsg = EmailMessage()
replymsg['From'] = receivedaddr
replymsg['To'] = replyaddr
replymsg['Subject'] = "Re: " + subject
if (messageid):
    replymsg['In-Reply-To'] = messageid

resp = chatbot.get_chat_response(msgbody, output="text")
logger.debug("Response to incoming email message: " + resp['message'])
replymsg.set_content(resp['message'])

#print(replymsg.as_string())
logger.debug("Created reply message: " + replymsg.as_string())

smtpserver = config['smtpserver']
logger.info("Sending reply message to '" + replymsg['To'] + "' from '" + replymsg['From'] + "' subject: '" + replymsg['Subject'] + "' via host " + smtpserver)

# Send the message via our own SMTP server.
s = smtplib.SMTP(smtpserver)
s.send_message(replymsg)
s.quit()
