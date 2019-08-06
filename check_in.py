import random
import datetime

class CheckIn:
    """Performs the check in and records the state of the individual.
    
    A check in is composed of multiple questions, each which will (hopefully) garner
    a response.
    """

    FUN_REACTS = [":dancingpanda:", ":dancing_corgi:", ":dancing_penguin:", ":party_docker:", ":tada:", ":fire:", ":popcorn_parrot:"]

    def __init__(self, channel):
        self.channel = channel
        self.username = "how you doin'"
        self.icon_emoji = ""
        self.timestamp = ""
        self.questions = [{
            "question": "How are we feelin' emotionally today?",
            "value": "emotion",
            "response_options": [{
                "title": ":cry:",
                "description": "Terrible"
            }, {
                "title": ":slightly_frowning_face:",
                "description": "Not great"
            }, {
                "title": ":neutral_face:",
                "description": "Okay"
            }, {
                "title": ":simple_smile:",
                "description": "Good"
            }, {
                "title": ":smile:",
                "description": "Great!"
            }],
            "response": "",
            "ts": ""
        }, {
           "question": "How are we feelin' energetically today?",
           "value": "energy",
           "response_options": [{
                "title": ":thumbsdown:",
                "description": "Low energy"
            }, {
                "title": ":neutral_face:",
                "description": "In-between"
            }, {
                "title": ":thumbsup:",
                "description": "High energy!"
            }],
           "response": "",
           "ts": ""
        }]
    
    def get_messages(self):
        messages = []

        welcome_text = f"Good afternoon! We have *{len(self.questions)} questions* for you today.\n\n"
        messages.append(self.get_message_payload(CheckIn.format_text_block(welcome_text)))
        
        for i, question in enumerate(self.questions):
            messages.append(self.get_message_payload(self._get_question_blocks(i)))
        return messages
    
    def get_message_payload(self, block):
        if not isinstance(block, list):
            block = [block]
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "text": "",
            "blocks": block,
        }
        
    def _get_question_blocks(self, question_index):
        blocks = []
        current_question = self.questions[question_index]
        text = f"{question_index + 1}) {current_question['question']} \n\n" 
        blocks.append(CheckIn.format_text_block(text))
        blocks.append(CheckIn.format_question_block(current_question))
        return blocks
    

    # BLOCK FORMATTING METHODS
    @staticmethod
    def format_text_block(text):
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

    @staticmethod
    def format_question_block(question_info):
        buttons = [CheckIn.format_response_option(r, i) for i, r in enumerate(question_info["response_options"])]
        return {
            "type": "actions",
            "elements": buttons,
            "block_id": question_info["value"]
        }
       
    
    @staticmethod
    def format_response_option(response_option, response_index):
        return {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": f"{response_option['title']} {response_option['description']}",
                "emoji": True
            },
            "value": str(response_index + 1),
            "action_id": str(response_index + 1)
        }