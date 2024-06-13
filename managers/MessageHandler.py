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
        
        if len(messageHistory) > 3:
            text = messageHistory[-2]['content'][0]['text']
            cleaned_text = re.sub(r'<current_collected_table>(.*?)</current_collected_table>', '', text)
            messageHistory[-2]['content'][0]['text'] = cleaned_text
            print("\nMessage History After Clean", messageHistory)
            
        return messageHistory

    def parse_bot_response(self,response):
        response_pattern = r'<Response>(.*?)</Response>'
        match = re.search(response_pattern, response, re.DOTALL)

        if match:
            response_text = match.group(1)
            return response_text
        else: #edge case issue with parsing
            return "I'm having some issues currently"
        
    def get_stored_table(self, response):
        table_pattern = r'<current_collected_table>(.*?)</current_collected_table>'
        match = re.search(table_pattern, response, re.DOTALL)

        if match:
            table_text = match.group(1)
            return table_text
        else: #edge case issue with parsing
            return "No stored table found"        

