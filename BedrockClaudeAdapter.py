import boto3
import json
import logging
from botocore.exceptions import ClientError
from langchain_community.embeddings import BedrockEmbeddings
# from .base import ModelAdapter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class BedrockClaudeAdapter():
    def __init__(self, model_id="anthropic.claude-3-sonnet-20240229-v1:0", region = 'us-east-1'):
        self.embeddings = BedrockEmbeddings(region_name=region)
        self.model_id = model_id
        self.client = boto3.client('bedrock-runtime', region)
        # super()._ init_(*args,**kwargs)

    def get_embeddings(self):
        return self.embeddings
    
    async def generate_llm_payload(self, system_prompt ,messages , max_token = 1000, temperature = 1):
        return {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_token,
            "temperature": temperature,
            "system": system_prompt,
            "messages": messages
        }
    
    async def get_llm_body(self, kb_data, chat_history, max_tokens=512, temperature=0.5):
        system_prompt = """You are a CIP assistant responsible for helping the user effectively communicate their potato germplasm needs to the CIP Gene Bank. Your goal is to gather all the necessary information from the user and formulate a comprehensive request to CIP, reducing the need for extended back-and-forth communication.
                            Ensure the following traits are gathered:

                            <Traits>
                                <trait_usage>
                                    <captured_text>Identify how the potatoes will be used in the user’s breeding program.</captured_text>
                                    <required>True</required>
                                </trait_usage>
                                <trait_color>
                                    <captured_text>Ask about the preferred color traits for the potato germplasm (yellow, green, white, or purple) if this information is not already provided.</captured_text>
                                    <required>True</required>
                                </trait_color>
                                <trait_temperature>
                                    <captured_text>Inquire about the desired heat adaptation traits for potatoes, especially for tropical regions.</captured_text>
                                    <required>True</required>
                                </trait_temperature>
                                <trait_location>
                                    <captured_text>Get the geographical location where the potatoes will be grown.</captured_text>
                                    <required>True</required>
                                </trait_location>
                                <trait_latitude>
                                    <captured_text>Optionally, ask for latitude coordinates to improve location precision.</captured_text>
                                    <required>False</required>
                                </trait_latitude>
                                <trait_longitude>
                                    <captured_text>Optionally, ask for longitude coordinates for accurate location data if not already provided.</captured_text>
                                    <required>False</required>
                                </trait_longitude>
                            </Traits>


                            Response Format:

                            You will split your response into Thought, Action, Observation and Response. Use this XML structure and keep everything strictly within these XML tags. Remember, the <Response> tag contains what's shown to the user. There should be no content outside these XML blocks. For each trait collected, build out a table containing those traits within a table having the following column: Trait, Question asked for the trait, The user response, whether the information is required or not, whether the order is important or not for the trait, possible valid answers.

                            <Thought> Your internal thought process. </Thought>
                            <Action> Your actions or analyses. </Action>
                            <Observation> User feedback or clarifications. </Observation>
                            <current_collected_table> The built out table so far. </current_collected_table>
                            <Response> Your communication to the user. This is the only visible portion to the user. </Response>

                            After collecting the essential traits, say the phrase 'Got everything I need'.
                            After confirming with the user say the phrase 'Request Submitted'.
                            """
        
        system_prompt = system_prompt.format(kb_data=kb_data)
        
        messages = []
        for message in chat_history:
            messages.append(message)
        
        bedrock_payload = await self.generate_llm_payload(system_prompt = system_prompt, messages = messages, max_tokens=max_tokens, temperature = temperature)
        return bedrock_payload

async def generate_response(self, llm_body):
    accept = 'application/json'
    contentType = 'application/json'

    response = self.client.invoke_model(body=llm_body, modelId=self.model_id, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    response_content = response_body['content'][0]['text']
    
    return response_content

