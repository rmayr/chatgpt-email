from revChatGPT.revChatGPT import Chatbot
import json
import email
import logging
import sys

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
logger.debug("Using login data: " + config["email"] + " / " + config["password"])

promptfile = open("queryprompt.txt", "r")
queryprompt = promptfile.read()
logger.debug("Prompt query for priming ChatGPT session: " + queryprompt)

newmsg = email.message_from_file(sys.stdin)
logger.debug("Processing new incoming email message: " + newmsg.as_string())


# TODO: use the email thread-id as conversation_id
chatbot = Chatbot(config, conversation_id=None)
#chatbot.reset_chat() # Forgets conversation
chatbot.refresh_session() # Uses the session_token to get a new bearer token
resp = chatbot.get_chat_response(queryprompt, output="text") # Sends a request to the API and returns the response by OpenAI
logger.debug("Response to query prompt: " + resp['message']) # The message sent by the response
#resp['conversation_id'] # The current conversation id
#resp['parent_id'] # The ID of the response

resp = chatbot.get_chat_response(newmsg.get_body('plain'), output="text")
print(resp['message'])

# # This returns a stream of text (live update)
#resp = chatbot.get_chat_response(prompt, output="stream") 
#for line in resp: # You have to loop through the response stream
#        print(line['message']) # Same format as text return type
#        ...
