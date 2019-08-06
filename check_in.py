import random

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
        self.current_question = 0
    
    def get_message_payload(self):
        if self.current_question < len(self.questions):
            notif_text = self.questions[self.current_question]["question"]
        else:
            notif_text = "That's all we have for today! See you next time!"

        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "text": notif_text,
            "blocks": self._get_question_block(),
        }

    def _get_question_block(self):
        blocks = []
        if self.current_question >= len(self.questions):
            blocks.append(CheckIn.format_text_block(f"That's all the questions we have for you today! See you next time {random.choice(self.FUN_REACTS)}\n"))
        else:
            if self.current_question == 0:
                blocks.append(CheckIn.format_text_block(f"Good afternoon! We have *{len(self.questions)} questions* for you today.\n\n"))
        
            current_question = self.questions[self.current_question]
            text = f"{self.current_question + 1}) {current_question['question']} \n\n" 
            blocks.append(CheckIn.format_text_block(text))
            blocks.append(CheckIn.format_question_block(current_question, self.current_question))
        return blocks
    

    # BLOCK FORMATTING METHODS
    @staticmethod
    def format_text_block(text):
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

    @staticmethod
    def format_question_block(question_info, question_index):
        buttons = [CheckIn.format_response_option(r) for r in question_info["response_options"]]
        return {
            "type": "actions",
            "elements": buttons,
            "block_id": f"question-{question_index}"
        }
       
    
    @staticmethod
    def format_response_option(response_option):
        return {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": f"{response_option['title']} {response_option['description']}",
                "emoji": True
            },
            "value": response_option['title']
        }