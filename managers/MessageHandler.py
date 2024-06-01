import re

class MessageHandler:
    def __init__(self) -> None:
        self.sessions = {}
    
    def humanChatFormat(self,prompt, messageHistory):
        human_chat_element = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }]
        }

        messageHistory.append(human_chat_element)

        return messageHistory


    def AIchatFormat(self,response, messageHistory):
        response_val = response

        AI_chat_element = {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": response_val
                }]
        }

        messageHistory.append(AI_chat_element)
        return messageHistory

    def parse_bot_response(self,response):
        response_pattern = r'<Response>(.*?)</Response>'
        match = re.search(response_pattern, response, re.DOTALL)

        if match:
            response_text = match.group(1)
            return response_text
        else: #edge case issue with parsing
            return "I'm having some issues currently"
        

