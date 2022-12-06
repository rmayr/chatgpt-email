from revChatGPT.revChatGPT import Chatbot
import json
import email
import logging

logger = logging.getLogger('chatgpt-email')
logger.setLevel(logging.DEBUG)

# example from https://github.com/acheong08/ChatGPT

# Get your config in JSON
configfile = f.open("config.json", "r")
config = configfile.readlines()

logger.debug("Using login data: " + config)

promptfile = f.open("queryprompt.txt", "r")
queryprompt = promptfile.readlines()

logger.debug("Prompt query for priming ChatGPT session: " + queryprompt)

newmsg = email.message_from_bytes(sys.stdin)

logger.debug("Processing new incoming email message: " + newmsg.as_string())



# TODO: use the email thread-id as conversation_id
chatbot = Chatbot(config, conversation_id=None)
chatbot.reset_chat() # Forgets conversation
chatbot.refresh_session() # Uses the session_token to get a new bearer token
resp = chatbot.get_chat_response(queryprompt, output="text") # Sends a request to the API and returns the response by OpenAI
#resp['message'] # The message sent by the response
#resp['conversation_id'] # The current conversation id
#resp['parent_id'] # The ID of the response

resp = chatbot.get_chat_response(newmsg.get_body('plain'), output="text") # Sends a request to the API and returns the response by OpenAI

# # This returns a stream of text (live update)
#resp = chatbot.get_chat_response(prompt, output="stream") 
#for line in resp: # You have to loop through the response stream
#        print(line['message']) # Same format as text return type
#        ...
